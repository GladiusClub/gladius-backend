# https://cloud.google.com/functions/docs/calling/firebase-auth

import firebase_admin
from firebase_admin import credentials, auth, firestore
from google.cloud import storage

from web3 import Web3
from datetime import datetime

import tempfile # transform Firebase SDK key file


import requests
from stellar_sdk import Keypair

def create_new_stellar_account():
    pair = Keypair.random()
    #print(f"Secret: {pair.secret}")
    print(f"Stellar public Key: {pair.public_key}")
    return pair

def activate_new_stellar_account(public_key):
    
    response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
    if response.status_code == 200:
        print(f"SUCCESS! You have a new account :)\n{response.text}")
    else:
        print(f"ERROR! Response: \n{response.text}")
    return response.text


def create_new_account():
    # Create new web3 accounts for the users
    infura_url = f"https://polygon-mumbai.infura.io/v3/668090c439f74210a8c15816a3ea83e2"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    if web3.isConnected():
        print("web3 is connected")
    else:
        print("Wow. Something went wrong with web3")

    return web3.eth.account.create()


# Cloud Function to create a Firestore document for a new user
def create_user_document(data, context):

    # Call this function to initialize the Firebase Admin SDK in your Cloud Function
    try:
        # Replace with your Cloud Storage bucket and the path to the service account credentials JSON file
        bucket_name = "gladius-backend"
        credentials_file_path = "firebase-admi-sdk-d55dc53a0acc.json"

        # Download the service account credentials JSON file from Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(credentials_file_path)
        credentials_file_content = blob.download_as_text()
        print(credentials_file_path + ' was downloaded from ' + bucket_name)

        # Initialize the Firebase Admin SDK with the downloaded service account credentials
               # Create a temporary file to write the credentials content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(credentials_file_content.encode())
            temp_file_path = temp_file.name 

        # Initialize the Firebase Admin SDK with the temporary file
        if not firebase_admin._apps:
            cred = credentials.Certificate(temp_file_path)
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        #cred = credentials.Certificate(credentials_file_content)
        # firebase_admin.initialize_app(cred)

        print('Firebase connection is up')

    except Exception as e:
        print("Error initializing Firebase Admin SDK:", e)

    try:

        email = data["email"]
        uid = data["uid"]
        print("Function triggered by creation of user: %s" % data["uid"])

        account = create_new_account()
        print(f"wallet created for {uid}")

        stellar_wallet = create_new_stellar_account()
        print(f"stellar wallet created for {uid}")
        activate_new_stellar = activate_new_stellar_account(stellar_wallet.public_key)
        
        user_record = auth.get_user(uid)
        display_name = user_record.display_name
        print(f"User {uid} display name is {display_name}")


        #Create a wallet
        # The data you want to save in Firestore
        user_data = {
            "email": email,
            "is_active": True,
            "clubs_roles": [],
            "address": account.address,
            "privateKey": account.key.hex(),
            "created_at": datetime.now(),
            "displayName": display_name,
            "name" : display_name,
            "stellar_wallet:" : stellar_wallet.secret,
            "stellar_secret:" : stellar_wallet.public_key
        }

        # Set the data in Firestore
        user_ref = db.collection("users").document(uid)
        user_ref.set(user_data)
        print(f"Successfully added user {display_name} {uid} to users collection")

    except Exception as e:
        print("Firebase Error:", e)

# Deploy the Cloud Function
# create_user_function = auth.user().on_create(create_user_document)