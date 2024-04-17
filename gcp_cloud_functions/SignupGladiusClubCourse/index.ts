import * as functions from 'firebase-functions';
import { db } from './scripts/firebaseAdminSetup.js';
import { Address, nativeToScVal, xdr, scValToNative } from 'stellar-sdk';
import { AddressBook } from './utils/address_book.js';
import {  getTotalCourses, getIsRole, invokeContract } from './utils/contract.js';
import { api_config } from './utils/api_config.js';
import { config } from './utils/env_config.js';


export const SignupGladiusClubCourse = functions.https.onRequest(async (request, response) => {
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
const folder = 'public'; 

const ClubOwnerUID: string = request.body.ClubOwnerUID; 
const ClubUID: string = request.body.ClubUID; 
const CourseName: string = request.body.CourseName; 
const CoursePrice: number = request.body.CoursePrice;
const Courseincentive: number = request.body.Courseincentive;

if (!ClubOwnerUID || !ClubUID) {
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

async function CreateCourse(
  addressBook: AddressBook,   
  club_stellar_secret: string,
  CourseName: string ,
  CoursePrice: number,
  Courseincentive: number 
) {


    let gladius_admin = loadedConfig.admin;
    const sport_club = api_config(network, club_stellar_secret);
  
  
    console.log('-------------------------------------------------------');
    console.log('Creating Gladius CLub and Course');
    console.log('-------------------------------------------------------');
  
    console.log('club public key: ', sport_club.publicKey());
    console.log("  🕵️  | Checking and Setting Roles");

    /*
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
  */
    
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
  
  console.log("  📝  | Checking and Creating Courses")

  const totalCoursesBefore = await getTotalCourses(
    addressBook.getContractId(network, 'gladius_subscriptions_id'),
    gladius_admin
    );
  console.log(" ~ testGladius ~ totalCoursesBefore:", totalCoursesBefore)

  const createCourseParams: xdr.ScVal[] = [
    new Address(sport_club.publicKey()).toScVal(), // sport_club
    nativeToScVal(CoursePrice, { type: 'i128' }), // price
    nativeToScVal(Courseincentive, { type: 'i128' }), // incentive
    nativeToScVal(CourseName, { type: 'string' }), // title
  ];
  const courseReponse = await invokeContract('gladius_subscriptions_id', addressBook, 'create_course', createCourseParams, sport_club);
  const courseIndex = scValToNative(courseReponse.returnValue);
  console.log("~ testGladius ~ courseIndex:", courseIndex)
  
  const totalCoursesAfter = await getTotalCourses(
    addressBook.getContractId(network, 'gladius_subscriptions_id'),
    gladius_admin
    );
  console.log(" ~ testGladius ~ totalCoursesAfter:", totalCoursesAfter)


  const getCourseParams: xdr.ScVal[] = [
    nativeToScVal(courseIndex, { type: 'u32' }), // index
  ];
  const gotCourse = await invokeContract('gladius_subscriptions_id', addressBook, 'get_course', getCourseParams, sport_club);
  const gotCourseNative = scValToNative(gotCourse.returnValue);
  console.log(" ~ testGladius ~ gotCourseNative:", gotCourseNative)
  

  console.log("   ")
  console.log("   ")
    
    
  }
  
  console.log("Connecting to firebase");
  
   //const ClubOwnerUID = 'lDGvMbJDEsOSX77KYZaaGD6suJH3'; 
  
    const userDocRef = db.collection('users').doc(ClubOwnerUID);
  
    const userDocSnap = await userDocRef.get();
  
    if (userDocSnap.exists) { 
      const userData = userDocSnap.data();
      if (userData && userData.stellar_wallet && userData.email) { 
        console.log(`ClubOwner doc with ID ${userData} was found. User email: `, userData.email);
        
        const club_owner_stellar_wallet = userData.stellar_wallet
        const club_owner_stellar_secret = userData.stellar_secret
        console.log("ClubOwner public key:", club_owner_stellar_wallet);
        
        await CreateCourse(addressBook, club_owner_stellar_secret, CourseName, CoursePrice ,Courseincentive);
        response.status(200).json({
          message: `Club owner ${userData.email} created a club ${userData.stellar_wallet}`,
          club_public_key: club_owner_stellar_wallet,
        });
  };
  }
          
  else {
    console.log(`club with ID ${ClubOwnerUID} not found `);
  }
});