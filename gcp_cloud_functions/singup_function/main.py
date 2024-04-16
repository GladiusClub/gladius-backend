# https://cloud.google.com/functions/docs/calling/firebase-auth

import firebase_admin
from firebase_admin import credentials, auth, firestore
from google.cloud import storage
from google.cloud import kms
from google.oauth2 import service_account
from cryptography.fernet import Fernet
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
        print(f"SUCCESS! Your stellar account was activated :) ")
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



def kms_decrypt_encryption_key(encrypted_encryption_key, KMS_KEY_FILE):
    print("Initiate KMS")
    project_id = 'wallet-login-45c1c'
    parent = f"projects/{project_id}/locations/global"
    key_ring_name = f"{parent}/keyRings/gladius-key-ring"
    key_name = f"{key_ring_name}/cryptoKeys/gladius-key"
    print(key_name)

    try:
        # Create the credentials object from the service account file.
        kms_credentials = service_account.Credentials.from_service_account_file(KMS_KEY_FILE)
        kms_client  = kms.KeyManagementServiceClient(credentials=kms_credentials)
        response = kms_client.decrypt(
        request={"name": key_name, "ciphertext": encrypted_encryption_key}
        )
        encryption_key = response.plaintext

        return encryption_key

    except Exception as e:
        print("Error in KMS client: ", e)



def download_file_from_bucket(bucket_name, credentials_file_path):
    try:
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
        
        return temp_file_path

    except Exception as e:
        print("Error downloading file from bucket: ", e)


# Cloud Function to create a Firestore document for a new user
def create_user_document(data, context):

    try:
        bucket_name = "gladius-backend"
        credentials_file_path = "firebase-admi-sdk-d55dc53a0acc.json"
        firebase_key_file = download_file_from_bucket(bucket_name, credentials_file_path)

        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_key_file)
            firebase_admin.initialize_app(cred)
        db = firestore.client()

        print('Firebase connection is up')

    except Exception as e:
        print("Error initializing Firebase Admin SDK:", e)
    
    try:
        # Specify the club ID and get a reference to the club document
        club_id = '2'
        club_ref = db.collection('clubs').document(club_id)

        # Fetch the document
        doc = club_ref.get()

        # Check if the document exists
        if doc.exists:
            # Access the encrypted_encryption_key field
            encrypted_encryption_key = doc.to_dict().get('encrypted_encryption_key', 'Default or error value')
            print("Encrypted Encryption Key loaded")
        else:
            print("Document does not exist.")
   
    except Exception as e:
        print("Error reading Encrypted Encryption Key:", e)
    
    try:
        encryption_key = kms_decrypt_encryption_key(encrypted_encryption_key, firebase_key_file)
        f = Fernet(encryption_key)
        
    except Exception as e:
        print("Error initializing Fernet client:", e)    

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
            "stellar_wallet" : stellar_wallet.secret,
            "encrypted_stellar_secret" : f.encrypt(stellar_wallet.secret.encode()),
            "stellar_secret" : stellar_wallet.public_key
        }

        # Set the data in Firestore
        user_ref = db.collection("users").document(uid)
        user_ref.set(user_data)
        print(f"Successfully added user {display_name} {uid} to users collection")

    except Exception as e:
        print("Firebase Error:", e)
