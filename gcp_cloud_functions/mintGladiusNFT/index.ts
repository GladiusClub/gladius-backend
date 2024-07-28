import * as functions from 'firebase-functions';
import { Request, Response } from 'express';  
import { Address, nativeToScVal, xdr } from  "@stellar/stellar-sdk";
import { auth, db } from './scripts/firebaseAdminSetup.js';
import { AddressBook } from './utils/address_book.js';
import { getTotalSupplyNFT, invokeContract } from './utils/contract.js';
import { api_config } from './utils/api_config.js';
import { config } from './utils/env_config.js';

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
  img_uri: string;
  to_address: string;
  
  
}

export const mintGladiusNFT = functions.https.onRequest(async (request, response) => {
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
              const img_uri = transaction.img_uri;

              await mintNFT(source_stellar_secret, to_address, img_uri, results);
              
              console.log(`Club ${userData.email} minted ${img_uri} to ${to_address}`)

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

async function mintNFT(sourceSecret: string, to_address:string, img_uri:string  , results: any[]): Promise<void> {
  const network: string = 'testnet';
  const addressBook = AddressBook.loadFromFile(network, 'public');
  //const sourceUser = api_config(network, sourceSecret);
  const sourceUser = api_config(network, 'SAOEGQCRNGEDGAZWTFIHLSVB6OWNFOCQKPAKP7NCAYE3ISMVSV34RUYR');
  const contractId: keyof ContractNames = 'gladius_nft_id';


  console.log("IPFS URI:" , img_uri);
  const totalSupplyNFT = await getTotalSupplyNFT(
    addressBook.getContractId(network, 'gladius_nft_id'),
    sourceUser
    );
  console.log("🚀 ~ testGladius ~ totalSupplyNFT:", totalSupplyNFT)

  const newIndex = Number(totalSupplyNFT) +1

  try {
     
    const mintNFTParams = [
      new Address(to_address).toScVal(), // to Andrei
      nativeToScVal(newIndex, { type: 'u32' }), // index
      nativeToScVal(img_uri, { type: 'string' }),
    ];

    await invokeContract(
      'gladius_nft_id',
      addressBook,
      'mint',
      mintNFTParams,
      sourceUser
    );
    results.push({ to_address: to_address, minted_uri: img_uri});

   } catch (error) {
    const message = (error as Error).message;
    throw new Error(`Error distributing mionting NFT: ${message}`);
  }
 
 }