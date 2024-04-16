import { Address, nativeToScVal, xdr } from 'stellar-sdk';
import * as functions from 'firebase-functions';
import { config } from './utils/env_config.js'; // Adjust the path as necessary
import { invokeContract } from './utils/contract.js'; // Import getTokenBalance
import { AddressBook } from './utils/address_book_api.js'; // Import AddressBook

export const StellarSorobanTransfer = functions.https.onRequest(async (req, res) => {
  try {
    // Extract 'network' and 'folder' from query parameters
    const network = req.query.network as string || 'testnet';
    const folder = req.query.folder as string || 'public';
    const publicKey = req.query.publicKey as string || 'GA2ZSBCXUKCOQLOMPLGAJ2JR2RBNC4UGFYKYIYO2VQEPJCNJ27I5E73L'; // Use the default if not provided


    let addressBook: AddressBook;
    addressBook = AddressBook.loadFromFile(network, folder);
   

    const loadedConfig = config(network);
    let student = loadedConfig.getUser('STUDENT_SECRET');

    const transactionParams: xdr.ScVal[] = [
      new Address(student.publicKey()).toScVal(), // from
      new Address(publicKey).toScVal(), // to
      nativeToScVal(1000, { type: 'i128' }), // amount
    ];
    
    let transferGLC = await invokeContract('gladius_emitter_id', addressBook, 'transfer', transactionParams, student);
   

    res.status(200).send(`GLC sent from ${student.publicKey()}  to ${publicKey}: ${transferGLC}`);
  } catch (error) {
    console.error('Failed to send GLC:', error);
    res.status(500).send('Internal Server Error');
  }
  
});