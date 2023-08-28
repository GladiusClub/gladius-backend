// https://stackoverflow.com/questions/47659525/creating-a-document-in-firestore-using-cloud-functions


const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();


exports.createProfile = functions.auth.user().onCreate((user) => {

  var userObject = {
     // displayName : user.displayName,
     email : user.email,
  };

  return admin.firestore().doc('users/'+user.uid).set(userObject);
 // or admin.firestore().doc('users').add(userObject); for auto generated ID 

})