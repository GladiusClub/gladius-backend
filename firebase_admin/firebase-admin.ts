import * as admin from 'firebase-admin';
import { ServiceAccount } from 'firebase-admin';

// Replace './path/to/serviceAccountKey.json' with the actual path to your service account key file
import serviceAccount from '../firebase-adminsdk.json' assert { type: 'json' };


admin.initializeApp({
  credential: admin.credential.cert(serviceAccount as ServiceAccount),
  databaseURL: "https://wallet-login-45c1c-default-rtdb.europe-west1.firebasedatabase.app"
});

const db = admin.firestore();

const docId = '0ugnaHneIdThw5CUCFeAw7zMAZB2';
db.collection('users').doc(docId).get()
  .then(doc => {
    if (doc.exists) {
      console.log(doc.data()); // Logs the entire document data
    } else {
      console.log('No such document!');
    }
  })
  .catch(error => {
    console.error('Error getting document:', error);
  });
