import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';
import { getAuth } from 'firebase-admin/auth';


const app = initializeApp({
  credential: applicationDefault(),
  projectId: 'wallet-login-45c1c',
});

const db = getFirestore(app);
const auth = getAuth(app);

export {
  db,
  auth
};