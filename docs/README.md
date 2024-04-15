# Gladius backend cloud functions

* [SignupGladiusParent](https://console.cloud.google.com/functions/details/europe-west1/SignupGladiusParent?env=gen2\&project=wallet-login-45c1c) - parameters StudentUID, ParentUID, ClubUID, GroupUID
*
  * [Source ](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/SignupGladiusParent/index.ts)
  * [How to call ](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/SignupGladiusParent/test\_cf.sh)
* [fetchGladiusNFT](https://console.cloud.google.com/functions/details/europe-west1/fetchGladiusNFT?env=gen2\&project=wallet-login-45c1c) - UID (NFT image is hardcoded at the moment)
*
  * [Source ](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/fetchGladiusNFT/index.js)
  * [How to call](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/fetchGladiusNFT/test\_cf.sh)
* [getStudentBalanceByID](https://console.cloud.google.com/functions/details/europe-west1/getStudentBalanceByID?env=gen2\&project=wallet-login-45c1c) - UID
*
  * Source
* transferGLC - UID of sender and amount (by default sends GLC to club wallet, this can be changed)
*
  * [Source](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/invokeGladiusTransaction/index.js)
  * [How to call](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/invokeGladiusTransaction/test\_cf.sh)&#x20;
* Cloud function triggers
*
  * [Firebase\_auth\_sync](https://console.cloud.google.com/functions/details/us-central1/firebase\_auth\_sync?env=gen1\&project=wallet-login-45c1c) - triggers Firebase Authentication. Creates user doc from Firebase Auth. Create wallets [source](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/singup\_function/main.py)
  * [Delete\_user\_document](https://console.cloud.google.com/functions/details/us-central1/delete\_user\_document?env=gen1\&project=wallet-login-45c1c) - triggers Firebase Authentication. Deletes user doc when account is deleted from Firebase Auth
  * [Firestore\_sync\_users](https://console.cloud.google.com/functions/details/us-central1/firestore\_sync\_users?env=gen1\&project=wallet-login-45c1c) - triggers Cloud Firestore doc change. Sync clubs\_roles field in /users doc and members docs in /clubs [source](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/firebase\_sync/main.py)
