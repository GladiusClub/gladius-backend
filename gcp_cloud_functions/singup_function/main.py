from flask import request, jsonify

import firebase_admin
from firebase_admin import auth, credentials, firestore
from google.cloud import storage

from web3 import Web3
#from dotenv import load_dotenv
from datetime import datetime
import json
#from main import register_user

import tempfile # transform Firebase SDK key file
import functions_framework #  Enable CORS



def create_new_account():
    # Create new web3 accounts for the users
    infura_url = f"https://polygon-mumbai.infura.io/v3/668090c439f74210a8c15816a3ea83e2"
    web3 = Web3(Web3.HTTPProvider(infura_url))

    if web3.isConnected():
        print("web3 is connected")
    else:
        print("Wow. Something went wrong with web3")

    return web3.eth.account.create()

@functions_framework.http
def register_user(request):
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST",  # Allow both GET and POST methods
            "Access-Control-Allow-Headers": "Content-Type, Authorization",  # Added 'Authorization'
            "Access-Control-Max-Age": "3600",
        }


        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, Authorization"}
    
    # Parse JSON request data
    request_json = request.get_json()

    user = request_json.get('user')
    email = request_json.get('email')
    password = request_json.get('password')
    
    

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
    
     # Create Firebase Authentication user
    try:
        user_record = auth.create_user(
            email=email,
            password=password
        )
        user_uuid = user_record.uid
        print(f'Successfully created new user: {user_uuid}')

    except firebase_admin.auth.AuthError as e:
        # Handle any errors
        print(f'Error creating new user: {e}')
        return 'Error creating new user', 500
        # Create user account and data
    
    account = create_new_account()
    user_data = {
        "name": user,
        "email": email,
        "age": 25,
        "occupation": "Coach",
        "is_active": True,
        "clubs_roles": [],
        "address": account.address,
        "privateKey": account.key.hex(),
        "created_at": datetime.now()
    }

    try:
        users_collection = db.collection('users')
        user_ref = users_collection.document(user_uuid)
        user_ref.set(user_data)
        print(f"Successfully added user {user_uuid} to users collection")
    except Exception as e:
        print(f'Error inserting user data: {e}')
        return 'Error inserting user data', 500

    return 'User registered successfully', 200
