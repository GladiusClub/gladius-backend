import * as functions from 'firebase-functions';
import { Address, nativeToScVal, xdr } from 'stellar-sdk';
import { db } from './scripts/firebaseAdminSetup.js';
import { AddressBook } from './utils/address_book.js';
import { getTokenBalance, invokeContract } from './utils/contract.js';
import { api_config } from './utils/api_config.js';

export const transferGLC = functions.https.onRequest(async (request, response) => {
  // Set CORS headers for preflight requests
  response.set('Access-Control-Allow-Origin', 'http://localhost:3000');
  response.set('Access-Control-Allow-Methods', 'GET, POST');
  response.set('Access-Control-Allow-Headers', 'Content-Type');
  response.set('Access-Control-Max-Age', '3600');

  if (request.method === 'OPTIONS') {
    response.status(204).send('');
    return;
}

  const network = process.argv[2] || 'testnet';     

  const from_uid: string = request.body.from_uid; // Extract UID from the request body
  const to_uid: string = request.body.to_uid;
  const amount_str: string = request.body.amount; // Extract and parse the amount from the request body

  console.log(`Received FROM_UID:${from_uid}, TO_UID:${to_uid},  amount:${amount_str} `)

  const amount: number = Number(amount_str);
  const UID : string = from_uid;


  if ( !to_uid ||!from_uid || isNaN(amount)) {
    response.status(400).send('Missing or invalid parameters.');
    return;
  }

  let addressBook: AddressBook;
  const folder = 'public'; 

  if (folder === 'public') {
    addressBook = AddressBook.loadFromFile(network, folder);
  } else {
    addressBook = AddressBook.loadFromFile(network);
  }

 
  async function handleTransfer(source_stellar_secret: string, dest_stellar_secret: string) {
    
    const source_user = api_config(network, source_stellar_secret);
    const SourcePublicKey = source_user.publicKey(); 

    const dest_user = api_config(network, dest_stellar_secret);
    const DestPublicKey =  dest_user.publicKey();
    console.log("ContractId: ", addressBook.getContractId(network, 'gladius_emitter_id'))
    const sender_balance = await getTokenBalance(
      addressBook.getContractId(network, 'gladius_emitter_id'), // what token
      SourcePublicKey, // balance of who?
      source_user //who pays for transaction
    );

    console.log("Sender balance ", sender_balance)
    const courseIndex = 0;
    console.log("~ handleStudentOperations ~ courseIndex:", courseIndex);
    console.log("  ↔️   | Gladius Coins Transaction")
    
    //const min_dist = 10;
    //const max_dist = 15;
    //const amount = Math.floor(Math.random() * (min_dist - max_dist + 1)) + min_dist;
    
    console.log("      | Student Sends GLC to Sport Club: ", amount)

    const transactionParams: xdr.ScVal[] = [
      new Address(SourcePublicKey).toScVal(), // from
      new Address(DestPublicKey).toScVal(), // to
      nativeToScVal(amount, { type: 'i128' }), // amount
    ];

    if (amount < 0) {
      console.log('ERROR: Amount should be a positive number')
      response.status(400).send({ to_address: SourcePublicKey, error: 'Amount should be a positive number' });;
      return;

    } else if (amount === 0) {
      console.log('ERROR: Not allowed to send 0 coins')
      response.status(400).send({ to_address: SourcePublicKey, error: 'Not allowed to send 0 coins' });;
      return;

    } else if (DestPublicKey === SourcePublicKey) {
      console.log('ERROR: Not allowed to send coins to yourself')
      response.status(400).send({ to_address: SourcePublicKey, error: 'Not allowed to send coins to yourself' });;
      return;
      
    } else if (sender_balance < amount) {
      console.log('ERROR: Transfer amount exceeds balance')
      response.status(400).send({ to_address: SourcePublicKey, error: 'Transfer amount exceeds balance' });
      return;
      
    } else {
      // If all checks passed, perform the transaction
      try {
      console.log("invokeContract");
      await invokeContract('gladius_emitter_id', addressBook, 'transfer', transactionParams, source_user);
      console.log("Success");
      const sender_balance_after = await getTokenBalance(
        addressBook.getContractId(network, 'gladius_emitter_id'), // what token
        SourcePublicKey, // balance of who?
        source_user //who pays for transaction
      );
      console.log("Sender balance after", sender_balance_after)

     return response.status(200).json({ from_address: SourcePublicKey, to_address: DestPublicKey, sent: amount }); // Indicating success
      //message: `GLC sent form ${stellar_wallet} to ${club_stellar_wallet} in the amount of ${amount}`
      
    } catch (error) {
      const errorMessage = (error as Error).message;
      console.error(`Error invoking contract for address ${SourcePublicKey}: ${errorMessage}`);
      
      response.status(400).send({ from_address: SourcePublicKey, to_address: DestPublicKey, error: `Contract invocation failed: ${errorMessage}` });
      return // Indicating a client-side error
    }
  
  
  }
   
}

  console.log("Connecting to firebase");
  
  const FromRef = db.collection('users').doc(from_uid);
  const FromDocSnap = await FromRef.get();

  const ToRef = db.collection('users').doc(to_uid);
  const ToDocSnap = await ToRef.get();

  if (FromDocSnap.exists) { 
    const FromUserData = FromDocSnap.data();
    if (FromUserData && FromUserData.stellar_wallet && FromUserData.email) { // Check if userData is truthy before accessing its properties
      console.log(`Source ID ${from_uid} found. User email: ${FromUserData.email}`);
      
      const source_stellar_wallet = FromUserData.stellar_wallet
      const source_stellar_secret = FromUserData.stellar_secret
      console.log("proccess stellar wallet:", source_stellar_wallet);

      if (ToDocSnap.exists) {
        const ToUserData = ToDocSnap.data();
        if (ToUserData && ToUserData.stellar_wallet && ToUserData.email) {
          console.log(`Destination ID ${to_uid} was found.  User email: ${FromUserData.email}`);
          
          const dest_stellar_wallet = ToUserData.stellar_wallet
          const dest_stellar_secret = ToUserData.stellar_secret
          console.log(`Destination wallet ${dest_stellar_wallet} `);
          await handleTransfer(source_stellar_secret, dest_stellar_secret)
          
          console.log( `GLC sent form ${source_stellar_wallet} to ${dest_stellar_wallet} in the amount of ${amount}` );
        }
        

      }
      else {console.log(`Destination with ID ${to_uid} not found `);}
      
    }
  } else {
    console.log(`No source doc found with ID ${UID}`);
  }
  
  
});

