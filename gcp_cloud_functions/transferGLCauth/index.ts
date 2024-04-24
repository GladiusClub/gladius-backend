import * as functions from 'firebase-functions';
import { Request, Response } from 'express';  
import { Address, nativeToScVal, xdr } from 'stellar-sdk';
import { auth, db } from './scripts/firebaseAdminSetup.js';
import { AddressBook } from './utils/address_book.js';
import { getTokenBalance, invokeContract } from './utils/contract.js';
import { api_config } from './utils/api_config.js';

interface UserData {
  stellar_wallet: string;
  stellar_secret: string;
  email: string;
}

interface Transaction {
  to_address: string;
  amount: string;
}

export const transferGLC = functions.https.onRequest(async (request, response) => {
  // Set CORS headers for preflight requests
  response.set('Access-Control-Allow-Origin', 'http://localhost:3000');
  response.set('Access-Control-Allow-Methods', 'GET, POST');
  response.set('Access-Control-Allow-Headers', 'Content-Type');
  response.set('Access-Control-Max-Age', '3600');

  if (request.method === 'OPTIONS') {
      response.status(204).send();
      return;
  }

  if (!request.headers.authorization || !request.headers.authorization.startsWith('Bearer ')) {
      console.error('No Firebase ID token was passed as a Bearer token in the Authorization header.');
      response.status(403).send('Unauthorized: No Firebase ID token in Authorization header.');
      return;
  }

  const idToken = request.headers.authorization.split('Bearer ')[1];
  try {
      const decodedToken = await auth.verifyIdToken(idToken);
      const from_uid = decodedToken.uid;
      const transactions: Transaction[] = request.body.transactions;

      const userDoc = await db.collection('users').doc(from_uid).get();
      if (!userDoc.exists) {
          response.status(404).send('User not found.');
          return;
      }

      const userData = userDoc.data();
      if (!userData || !userData.stellar_wallet || !userData.stellar_secret || !userData.email) {
          response.status(404).send('User wallet details missing.');
          return;
      }
      console.log("Found user: ", userData.email )

      const source_stellar_secret = userData.stellar_secret;
      let results = [];
      for (const transaction of transactions) {
          try {
              const to_address = transaction.to_address;
              const amount = Number(transaction.amount);
              if (isNaN(amount) || amount <= 0) {
                  throw new Error('Invalid amount: Amount must be a positive number.');
              }
              await handleTransfer(source_stellar_secret, to_address, amount, results);
          } catch (error) {
              results.push({ error: error, to_address: transaction.to_address });
          }
      }

      response.status(200).send(results);
  } catch (error) {
      const message = (error as Error).message;
      console.error('Error verifying Firebase ID token:', message);
      response.status(403).send('Unauthorized: Token verification failed or server error occurred.');
  }
});

async function handleTransfer(sourceSecret: string, toAddress: string, amount: number, results: any[]): Promise<void> {
  const network: string = 'testnet';
  const addressBook = AddressBook.loadFromFile(network, 'public');
  const sourceUser = api_config(network, sourceSecret);
  const sourcePublicKey = sourceUser.publicKey();

  const senderBalance = await getTokenBalance(addressBook.getContractId(network, 'gladius_emitter_id'), sourcePublicKey, sourceUser);

  if (toAddress === sourcePublicKey) {
      throw new Error('Transaction error: Cannot send coins to the same address.');
  } else if (senderBalance < amount) {
      throw new Error('Transaction error: Transfer amount exceeds balance.');
  }

  try {
      const transactionParams: xdr.ScVal[] = [
          new Address(sourcePublicKey).toScVal(),
          new Address(toAddress).toScVal(),
          nativeToScVal(amount, { type: 'i128' })
      ];
      await invokeContract('gladius_emitter_id', addressBook, 'transfer', transactionParams, sourceUser);
      results.push({ from_address: sourcePublicKey, to_address: toAddress, sent: amount });
  } catch (error) {
      const message = (error as Error).message;
      throw new Error(`Error sending ${amount} to ${toAddress}: ${message}`);

  }
}