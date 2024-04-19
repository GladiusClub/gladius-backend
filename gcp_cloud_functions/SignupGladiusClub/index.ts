
import * as functions from 'firebase-functions';
import { FieldValue } from 'firebase-admin/firestore';
import { db } from './scripts/firebaseAdminSetup.js';
import { Address, nativeToScVal, xdr, scValToNative, Keypair, Networks, StrKey } from 'stellar-sdk';
import { AddressBook } from './utils/address_book.js';
import {  getIsRole, invokeContract } from './utils/contract.js';
import { api_config } from './utils/api_config.js';
import { config } from './utils/env_config.js';



const allowedOrigins = [
  'http://localhost:3000',
  'https://gladius-frontend.web.app',
];

export const SignupGladiusClub = functions.https.onRequest(async (request, response) => {

//response.set('Access-Control-Allow-Origin', 'http://localhost:3000');
  const origin: string = request.headers.origin || 'http://localhost:3000';
  if (allowedOrigins.includes(origin)) {
    response.set('Access-Control-Allow-Origin', origin) ;
 }
  
  response.set('Access-Control-Allow-Methods', 'GET, POST');
  response.set('Access-Control-Allow-Headers', 'Content-Type');
  response.set('Access-Control-Max-Age', '3600');

  if (request.method === 'OPTIONS') {
    response.status(204).send('');
    return;
}

const network = process.argv[2] || 'testnet';     
const folder = 'public'; 

const ClubOwnerUID: string = request.body.ClubOwnerUID; // Extract StudentUID from the request body
const ClubName: string = request.body.ClubName;


if (!ClubOwnerUID || !ClubOwnerUID) {
  response.status(400).send('Missing or invalid parameters.');
  return;
}


let addressBook: AddressBook;
const loadedConfig = config(network);

if (folder == 'public') {
    addressBook = AddressBook.loadFromFile(network, folder);
} else {
    addressBook = AddressBook.loadFromFile(network);
}

async function ClubSignupGladius(addressBook: AddressBook,   club_stellar_secret: string) {


    let gladius_admin = loadedConfig.admin;
    const sport_club = api_config(network, club_stellar_secret);
  
  
    console.log('-------------------------------------------------------');
    console.log('Creating Gladius CLub and Course');
    console.log('-------------------------------------------------------');
  
    console.log('club public key: ', sport_club.publicKey())
    console.log("  🕵️  | Checking and Setting Roles")
    
    const isSportClubBefore = await getIsRole(
      addressBook.getContractId(network, 'gladius_subscriptions_id'),
      'is_sport_club',
      sport_club.publicKey(),
      sport_club
      );
    
  
    console.log("~ testGladius ~ isSportClubBefore:", isSportClubBefore)
    console.log("   ")
  
    const setIsSportClubParams: xdr.ScVal[] = [
      new Address(sport_club.publicKey()).toScVal(), // sport_club
      nativeToScVal(true, { type: 'bool' }), // is
    ];
    
    await invokeContract('gladius_subscriptions_id', addressBook, 'set_is_sport_club', setIsSportClubParams, gladius_admin);
  
    
    const isSportClubAfter = await getIsRole(
      addressBook.getContractId(network, 'gladius_subscriptions_id'),
      'is_sport_club',
      sport_club.publicKey(),
      sport_club
      );
   
    console.log("   ")
  
    console.log("~ testGladius ~ isSportClubAfter:", isSportClubAfter)
  
    console.log("   ")
    console.log("   ")
  
    
    
  }
  
  console.log("Connecting to firebase");
  
    //const ClubOwnerUID = 'lDGvMbJDEsOSX77KYZaaGD6suJH3'; 
    //const ClubName = 'Test Club';

    const userDocRef = db.collection('users').doc(ClubOwnerUID);
  
    const userDocSnap = await userDocRef.get();
  
    if (userDocSnap.exists) { 
      const userData = userDocSnap.data();
      if (userData && userData.stellar_wallet && userData.email) { 
        console.log(`ClubOwner doc with ID ${userData} was found. User email: `, userData.email);

        // Data to be used in the new club document        
         const { stellar_wallet, stellar_secret } = userData;

         // Create a new club document with a random UID
         const clubDocRef = db.collection('clubs').doc();
         await clubDocRef.set({
             name: ClubName,
             club_stellar_wallet: stellar_wallet,
             club_stellar_secret: stellar_secret,
             gladius_subscriptions_id: addressBook.getContractId(network, 'gladius_subscriptions_id')
         });

        // Add club role to the user's document
        const clubRole = { club_id: clubDocRef.id, role: 'owner' };
        await userDocRef.update({
          clubs_roles: FieldValue.arrayUnion(clubRole)
      });
        console.log(`New club created with UID ${clubDocRef.id} and the owner has been updated.`);
          
        const club_owner_stellar_wallet = userData.stellar_wallet
        const club_owner_stellar_secret = userData.stellar_secret

        console.log("ClubOwner public key:", club_owner_stellar_wallet);
        
        await ClubSignupGladius(addressBook, club_owner_stellar_secret);
        
       
        response.status(200).json({
          message: `Club owner ${userData.email} created a club ${userData.stellar_wallet}`,
          data: {
          club_public_key: club_owner_stellar_wallet, 
          club_name: ClubName,
          club_uid: clubDocRef.id,
          gladius_subscriptions_id: "c8b70c1f05c748873ae9765a1ec350dbaba452cd3d32b88fedb8425858faa359",
        }
        });
  } else {
    console.log('Required user data is missing. No action taken.');
  };
  }
          
  else {
    console.log(`club with ID ${ClubOwnerUID} not found `);
  }
});