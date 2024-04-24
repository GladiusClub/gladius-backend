import * as functions from 'firebase-functions';
import { db } from './scripts/firebaseAdminSetup.js';
import { AddressBook } from './utils/address_book_api.js';
import { getTokenBalance } from './utils/contract.js';
import { api_config } from './utils/api_config.js';
const allowedOrigins = [
    'http://localhost:3000',
    'https://gladius-frontend.web.app',
    'https://gladius-club.web.app'
];
const isAllowedOrigin = (origin) => {
    // Check if the origin is exactly in the list of allowed origins
    if (allowedOrigins.includes(origin)) {
        return true;
    }
    // Check if the origin matches the pattern for allowed subdomains of gladius-frontend with any TLD
    if (/https:\/\/gladius-frontend[^\s]+\.web\.app/.test(origin)) {
        return true;
    }
    return false;
};
export const getStudentBalanceByID = functions.https.onRequest(async (request, response) => {
    // Set CORS headers for preflight requests
    // response.set('Access-Control-Allow-Origin', 'http://localhost:3000');
    const origin = request.headers.origin;
    if (isAllowedOrigin(origin)) {
        response.set('Access-Control-Allow-Origin', origin);
    }
   else {
        console.error('Origin not allowed by CORS policy:', origin);
        response.set('Access-Control-Allow-Origin', 'http://localhost:3000'); 
    }
    response.set('Access-Control-Allow-Methods', 'GET, POST');
    response.set('Access-Control-Allow-Headers', 'Content-Type');
    response.set('Access-Control-Max-Age', '3600');
    if (request.method === 'OPTIONS') {
        response.status(204).send('');
        return;
    }
    const network = process.argv[2] || 'testnet';
    const UID = request.body.UID; // Extract UID from the request body
    let addressBook;
    const folder = 'public';
    if (folder === 'public') {
        addressBook = AddressBook.loadFromFile(network, folder);
    }
    else {
        addressBook = AddressBook.loadFromFile(network);
    }
    console.log("Connecting to firebase");
    // const UID = '4KKWdVfzUcUcJf9mVSVdPRXSNLI2'
    const docRef = db.collection('users').doc(UID);
    const club_id = '2';
    const clubRef = db.collection('clubs').doc(club_id);
    const docSnap = await docRef.get();
    const clubSnap = await clubRef.get();
    if (docSnap.exists) {
        const userData = docSnap.data();
        if (userData && userData.stellar_wallet && userData.email) { // Check if userData is truthy before accessing its properties
            console.log(`Document with ID ${UID} found. User email: `, userData.email);
            const stellar_wallet = userData.stellar_wallet;
            const user_stellar_secret = userData.stellar_secret;
            console.log("proccess stellar wallet:", stellar_wallet);
            if (clubSnap.exists) {
                const clubData = clubSnap.data();
                if (clubData && clubData.name && clubData.club_stellar_secret && clubData.club_stellar_wallet) {
                    console.log(`Club ID ${club_id} was found. It's ${clubData.name} `);
                    const club_stellar_wallet = clubData.club_stellar_wallet;
                    const club_stellar_secret = clubData.club_stellar_secret;
                    console.log(`Club wallet ${club_stellar_wallet} `);
                    const student = api_config(network, user_stellar_secret);
                    const studentPublicKey = student.publicKey();
                    const sport_club = api_config(network, club_stellar_secret);
                    const clubPublicKey = sport_club.publicKey();
                    let balanceGLCStudent = await getTokenBalance(addressBook.getContractId(network, 'gladius_emitter_id'), studentPublicKey, sport_club);
                    response.status(200).json({
                        message: `GLC Balance of ${userData.email}`,
                        data: balanceGLCStudent
                    });
                }
            }
            else {
                console.log(`club with ID ${club_id} not found `);
            }
        }
    }
    else {
        console.log(`No document found with ID ${UID}`);
    }
});
