# Gladius backend cloud functions

## Gladius backend functional setup

### &#x20;Gladius Club Sign-up

#### &#x20;1. create club owner user  cloud function

**Purpose**

This Firebase function facilitates the sign-up process for the Gladius Club Owner user

&#x20;**frontend**

\- creates an auth record and email and UID

\- frontend calling /users collections and waiting for a user doc to appear

**backend**

\- triggers Auth create record and creates doc ( in /users) with stellar wallet

[trigger source code](../gcp\_cloud\_functions/firebase\_sync/main.py)

&#x20;



#### 2. set club owner in the contract  cloud function

[source code](../gcp\_cloud\_functions/SignupGladiusClub/index.ts)

**Purpose**

This Firebase function facilitates the sign-up process for the Gladius Club. It integrates with Firebase Firestore for user verification and the Stellar blockchain for role management within a sports club context.

&#x20;**frontend**

\- calls CF SignupGladiusClub

[https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusClub](https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusClub) &#x20;

Request Body Parameters

`'{ "ClubOwnerUID": "9UY6EVSrd0XDAHFBdt8sRpGsxLw1",`

&#x20;`"ClubName" : "Chess club"   }'`

&#x20;

**backend**

\- receives ClubOwnerUID, ClubName

\- creates club doc in /clubs with unique clubUID

\- sets the club\_name in club doc based on ClubName

\- copies stellar wallet public and private keys from /users doc(ClubOwnerUID) to /clubs/{clubUID}

\- sets role = “owner” in club\_roles under /users doc(ClubOwnerUID)

\- executes Gladius contract Soroban function “set\_is\_sport\_club“\
[https://testnet.stellarchain.io/operations/4843481864359937](https://testnet.stellarchain.io/operations/4843481864359937)

Returns: club\_owner\_UID has been added to club\_doc\_UID

`{  "message": "Club owner [user email] created a club [club public key]",`

&#x20; `"club_public_key": "[Club owner's Stellar public key]"}`

&#x20;&#x20;



#### 3.5 add calendar to the club

·         Frontend adds a calendar link to a new club doc



#### &#x20; 4. create course cloud function

[source code](../gcp\_cloud\_functions/SignupGladiusClubCourse/index.ts)

**Purpose**

Handles the creation of a new course within a sports club on the Stellar blockchain, leveraging Firebase Firestore for user authentication and management.

&#x20;**frontend**

\- calls CF SignupGladiusClubCourse

[https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusClubCourse](https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusClubCourse)

Request Body Parameters (example)

`{  "ClubOwnerUID": "MmNNhkPnhXfluJ0HMpwCFFImpLt2",`

&#x20; `"ClubUID" : "4",`

&#x20; `"CourseName" : "My awesome course",`

&#x20; `"CoursePrice" : 200,`

&#x20; `"Courseincentive" : 15,`

&#x20; `"CourseIndex" : 8 }'`

**backend**

\- Ensures required parameters (ClubOwnerUID, ClubUID, CourseName, CoursePrice, Courseincentive) are provided in the request body.

\- executes create\_course function with provided parameters

[https://testnet.stellarchain.io/operations/4852161993261057](https://testnet.stellarchain.io/operations/4852161993261057)

**Returns**

`{"message":"Club owner [user email]  created a club [club public key]","club_public_key":"[Club owner's Stellar public key]"`

&#x20;&#x20;



#### 5. add student to club  cloud function

[source code](../gcp\_cloud\_functions/SignupGladiusParent/index.ts)

Purpose: Manages the role assignment and course subscriptions for students and parents within a sports club ecosystem on the Stellar blockchain, facilitated through Firebase Firestore and Stellar smart contracts.

**frontend**&#x20;

\- creates parent and student Auth record

&#x20;  \-> wallets created automatically following logic described in (1)

\- calls [https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusParent](https://europe-west1-wallet-login-45c1c.cloudfunctions.net/SignupGladiusParent)

Request Body Parameters ([example](../gcp\_cloud\_functions/SignupGladiusParent/test\_cf.sh))

`{  "StudentUID": "exampleStudentUID",`

&#x20; `"ParentUID": "exampleParentUID",`

&#x20; `"ClubUID" : "exampleClubUID ",`

&#x20; `"GroupUID" : "exampleGroupUID " }`

**backend**

\-  Ensures required inputs (ParentUID, StudentUID, ClubUID, GroupUID) are provided and valid.

\-  Fetches and verifies necessary data from Firestore (for student, parent, and club)

\-   Executes contract functions with provided parameters

* Mints EURC to Parent
  * mintToken(addressBook.getContractId(network, 'token\_id'), 200, parent.publicKey(),  payment\_token\_admin);
* Sets and checks roles for both student and parent
* Registers and manages course subscriptions
  * invokeContract('gladius\_subscriptions\_id', addressBook, 'get\_course', getCourseParams, sport\_club);
  * invokeContract('gladius\_subscriptions\_id', addressBook, 'subscribe\_course', subscribeCourseParams, parent);
* Returns contract function response
  * Example response

`{  "message": "Student student@example.com was added to club ExampleClub by parent@example.com",`

`"parent_public_key":"GAXILOM5P7OQILZVUDGMBQXOUOFY2K5HOU6LHKBRL3TAIL3HABAODZMV",`

`"student_public_key":"GC3BQVW653PFYBRIXILV2MVVQQ4TCBQZ6FAQ3GO6PDFC3O64FAK3DO6Q",`

`"club_public_key":"GBHCD53TFM74SFTY4K2CQWGL6L2RR57Y5YPTFMOOJG5CE6EXDLGJVVYJ" }`





### Check student balance

#### 6. getStudentBalanceByID&#x20;

[ source code](../gcp\_cloud\_functions/getStudentBalanceByID/index.ts)

Endpoint [https://europe-west1-wallet-login-45c1c.cloudfunctions.net/getStudentBalanceByID](https://europe-west1-wallet-login-45c1c.cloudfunctions.net/getStudentBalanceByID)

&#x20;  \- Request Body Parameters (example)

`{  "StudentUID": "exampleStudentUID" }`

&#x20;  \- Response example

``{message: `GLC Balance of ${userData.email}`,   data: balanceGLCStudent }``

&#x20;



### Gladius Club NFT

#### 7. fetchGladiusNFT &#x20;

[source core](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/fetchGladiusNFT/index.ts)

&#x20;NFT image is hardcoded at the moment

**Purpose**

Retrieves Non-Fungible Tokens (NFTs) associated with a specific user within a sports club environment on the Stellar blockchain, using Firestore to manage user and club data

&#x20;  \- Endpoint [https://europe-west1-wallet-login-45c1c.cloudfunctions.net/fetchGladiusNFT](https://europe-west1-wallet-login-45c1c.cloudfunctions.net/fetchGladiusNFT)

\-NFT Data Retrieval: Executes a series of blockchain calls to:

* Get the number of NFTs owned by the user.
* Fetch each NFT's token ID and associated metadata URI.
* Retrieve and parse metadata from each URI to compile NFT details.

&#x20;  \-  Example request

`{  "UID": "exampleUserUID"}`

&#x20;  \- Execute: fetchGladiusNFT(addressBook, user\_stellar\_secret, club\_stellar\_secret);

&#x20;     \- Return response

&#x20;           {         message: \`GLC NFTs of ${userData.email}\`,

&#x20;                       data: fetchGladiusNFTresult  });

`Example response`

`{` &#x20;

`"message": "GLC NFTs of user@example.com",`

&#x20; `"data": {`

&#x20;   `"nfts": [`

&#x20;     `{ "name": "Gladius Token #1",`

&#x20;       `"image": "https://example.com/nft1.png",`

&#x20;       `"description": "This is a Gladius NFT 1"      },`

&#x20;     `{ "name": "Gladius Token #2",`

&#x20;       `"image": "https://example.com/nft2.png",`

&#x20;       `"description": "This is another Gladius NFT 2"  }  ]`

`}`



&#x20;

### Gladius coin (GLC) transfer

#### 8. transferGLC

&#x20;[Source code](../gcp\_cloud\_functions/invokeGladiusTransaction/index.js)

**Purpose**

Facilitates the transfer of Gladius Coins (GLC) between a student's account and a sports club's account on the Stellar blockchain, leveraging Firestore for user and club data management.

**Endpoint**

[https://europe-west1-wallet-login-45c1c.cloudfunctions.net/invokeGladiusTransaction](https://europe-west1-wallet-login-45c1c.cloudfunctions.net/invokeGladiusTransaction)

**Workflow**

User and Club Verification :Checks for necessary parameters (UID and amount), verifying that the amount is a valid number. By default sends GLC to club wallet (this can be changed).

Transaction Execution: Performs several checks before executing the token transfer:

* Ensures the transaction amount is positive and not zero.
* Confirms that the sender and receiver are not the same.
* Verifies that the sender's balance is sufficient to cover the transfer.
* Executes the transfer on the Stellar blockchain using smart contract interactions.

Example request:

`{  "UID": "exampleUserUID",   "amount": 100 }`

Example response

`{  "message": "GLC sent from GAXILOM5P7OQILZVUDGMBQXOUOFY2K5HOU6LHKBRL3TAIL3HABAODZMV to GBHCD53TFM74SFTY4K2CQWGL6L2RR57Y5YPTFMOOJG5CE6EXDLGJVVYJ in the amount of 100" }`



### Cloud function triggers

* [Firebase\_auth\_sync](https://console.cloud.google.com/functions/details/us-central1/firebase\_auth\_sync?env=gen1\&project=wallet-login-45c1c) - triggers Firebase Authentication. Creates user doc from Firebase Auth. Create wallets ( [source](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/singup\_function/main.py) )
* [Delete\_user\_document](https://console.cloud.google.com/functions/details/us-central1/delete\_user\_document?env=gen1\&project=wallet-login-45c1c) - triggers Firebase Authentication. Deletes user doc when account is deleted from Firebase Auth
* [Firestore\_sync\_users](https://console.cloud.google.com/functions/details/us-central1/firestore\_sync\_users?env=gen1\&project=wallet-login-45c1c) - triggers Cloud Firestore doc change. Sync clubs\_roles field in /users doc and members docs in /clubs ( [source](https://github.com/GladiusClub/gladius-backend/blob/app/testnet/gcp\_cloud\_functions/firebase\_sync/main.py) )

### Future work

Generate images with OpenAI API - [could function draft](./)

