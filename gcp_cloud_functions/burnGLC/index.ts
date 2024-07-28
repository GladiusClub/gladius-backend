import * as functions from 'firebase-functions';
import { Request, Response } from 'express';  
import { Address, nativeToScVal, xdr } from  "@stellar/stellar-sdk";
import { auth, db } from './scripts/firebaseAdminSetup.js';
import { AddressBook } from './utils/address_book.js';
import { getTokenBalance, invokeContract } from './utils/contract.js';
import { api_config } from './utils/api_config.js';

interface ContractNames {
    payment_token_admin_public: string;
    gladius_admin_public: string;
    token_id: string;
    gladius_emitter_id: string;
    gladius_subscriptions_id: string;
    gladius_nft_id: string;
  }

interface UserData {
  stellar_wallet: string;
  stellar_secret: string;
  email: string;
}

interface Transaction {
  amount: string;
  
  
}

export const burnGLC = functions.https.onRequest(async (request, response) => {
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
              const amount = Number(transaction.amount);

              if (isNaN(amount) || amount <= 0) {
                  throw new Error('Invalid amount: Amount must be a positive number.');
              } 

              await handleBurn(source_stellar_secret, amount, results);
              
              console.log(`Club ${userData.email} burned and unwrapped ${amount} GLC`)

          } catch (error) {
            const message = (error as Error).message;
              results.push({ error: message, club_address: userData.stellar_wallet});
          }
      }

      response.status(200).send(results);
  } catch (error) {
      const message = (error as Error).message;
      console.error('Error verifying Firebase ID token:', message);
      response.status(403).send('Unauthorized: Token verification failed or server error occurred.');
  }
});

async function handleBurn(sourceSecret: string, amount: number, results: any[]): Promise<void> {
  const network: string = 'testnet';
  const addressBook = AddressBook.loadFromFile(network, 'public');
  const sourceUser = api_config(network, sourceSecret);
  const sourcePublicKey = sourceUser.publicKey();
  const contractId: keyof ContractNames = 'gladius_emitter_id';

  let balanceGLCSportClub = await getTokenBalance(
    addressBook.getContractId(network, contractId), // what token
    sourceUser.publicKey(), // balance of who?
    sourceUser
  );

  console.log("« GLC  balance SportClub:", balanceGLCSportClub)
  if (balanceGLCSportClub < amount*1000) {
    throw new Error(`Transaction error: ${balanceGLCSportClub} GLC in not enough to burn  ${amount} EURC`);
  }
  
  try {
     
    const unwrapParams: xdr.ScVal[] = [
      new Address(sourceUser.publicKey()).toScVal(), // from
      nativeToScVal(amount, { type: 'i128' }), // unwrap_amount
    ];

    await invokeContract(contractId, addressBook, 'unwrap_and_burn', unwrapParams, sourceUser);

    results.push({ club_address: sourcePublicKey, burned: amount});

   } catch (error) {
    const message = (error as Error).message;
    throw new Error(`Error distributing gladius coins ${amount}: ${message}`);
  }
 
 }