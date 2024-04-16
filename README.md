# Gladius Backend 
## Setup  
Welcome to the Gladius Backend repository! 
Gladius backend is build based on [Google Firebase](https://firebase.google.com/).
If you havn't heard of Firebase before, please first refer to the [official Firebase docs](https://firebase.google.com/docs). 
Gladius backend is built on Cloud Firestore, which is part of Firebase ecosystem. Here are detailed instructions [how to get started with it](https://firebase.google.com/docs/firestore/quickstart)
## Gladius wallets
Gladius platform was designed with simplicity in mind with main focus on children and their parents. Our goal was to make the platform onboarding as simple and fast, as modern technology allows.
That is why we decided to use [custodial](https://infostride.com/custodial-and-non-custodial-wallets/) wallets creation model where our platform takes full responsibilty of wallet creation, private key encryption and signature provision when requested. 
Gladius wallets are created using standard [Stellar SDK](https://developers.stellar.org/docs/tutorials/create-account) and keys are secured in [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management) and additionally encrypted with [Fernet library](https://cryptography.io/en/latest/fernet/) 
Here is a [source code](https://github.com/GladiusClub/gladius-backend/blob/main/gcp_cloud_functions/singup_function/main.py) of wallet creation and encryption process. Feel free to contract us if you'll find in insufficient. 
## Gladius backend description
For detailed information about Gladius backend and additional documentation, please refer to the [documentation directory](./docs/README.md).

