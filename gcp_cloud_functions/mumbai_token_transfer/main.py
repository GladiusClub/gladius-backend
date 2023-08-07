import json
from web3 import Web3
from decimal import Decimal, getcontext

import firebase_admin
from firebase_admin import credentials, auth
from google.cloud import storage

from flask import request, jsonify

# Read the ABI data from GLCToken.json
with open('GLCToken.json', 'r') as file:
    contract_data = json.load(file)

# Set the precision for decimal calculations (adjust this based on your requirements)
getcontext().prec = 28


# Set up the Polygon (Mumbai) network
polygon_rpc_url = "https://rpc-mumbai.maticvigil.com"  # Replace with the appropriate RPC endpoint
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Replace with your wallet's private key
private_key = ""
wallet_address = '0x717320e0Ea465dD9ee7b0345219DB1A6b2884869'



def initialize_firebase_admin_sdk():

    try: 
        # Replace with your Cloud Storage bucket and the path to the service account credentials JSON file
        bucket_name = "gladius-backend"
        credentials_file_path = "firebase-admi-sdk-d55dc53a0acc.json"

        # Download the service account credentials JSON file from Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(credentials_file_path)
        credentials_file_content = blob.download_as_text()

        # Initialize the Firebase Admin SDK with the downloaded service account credentials
        cred = credentials.Certificate(credentials_file_content)
        firebase_admin.initialize_app(cred)

        # If the above doesn't work:
        # Create a temporary file and write the content of the credentials JSON to it
        # with open("/tmp/serviceAccountKey.json", "w") as tmp_file:
        #    tmp_file.write(credentials_file_content)

        # Initialize the Firebase Admin SDK with the downloaded service account credentials
        #cred = credentials.Certificate("/tmp/serviceAccountKey.json")
        #firebase_admin.initialize_app(cred)

    except Exception as e:
            print("Error initializing Firebase Admin SDK:", e)

def token_transfer(request):
    # Get the Firebase ID token from the Authorization header
    bearer_token = request.headers.get("Authorization")
    if not bearer_token:
        return jsonify({"error": "Authorization token not found"}), 401

    id_token = bearer_token.split(" ")[1]       
    # Call this function to initialize the Firebase Admin SDK in your Cloud Function
    initialize_firebase_admin_sdk()


    try:

        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)

        # Access user information from the decoded token
        uid = decoded_token["uid"]
        email = decoded_token["email"]
        # Add any other user-related data you need


        #####################################
        # Cloud Function logic start

        request_json = request.get_json()
        if request_json and 'to_address' in request_json and 'amount' in request_json:
            to_address = request_json['to_address']
            amount = request_json['amount']

            #  GLC Token contract address
            token_contract_address = "0x7A57269A63F37244c09742d765B18b1852078072"

            # Replace with the token decimals (usually 18 for most ERC20 tokens)
            token_decimals = 18

            # Convert the amount to the token's base unit
            amount_in_base_unit = int(amount * 10**token_decimals)

            # Create the transaction
            transaction = {
                'to': token_contract_address,
                'value': 0,
                'gas': 200000,
                'gasPrice': w3.toWei('10', 'gwei'),
                'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_address)),
                'data': w3.contract.encodeABI(fn_name='transfer', args=[to_address, amount_in_base_unit]),
            }

            # Sign the transaction
            signed_transaction = w3.eth.account.signTransaction(transaction, private_key)

            # Send the transaction
            tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        # Cloud Function logic end
        #####################################



        # Return a response to the client
        return jsonify({"message": "Success", "uid": uid, "email": email, "Transaction sent. Transaction hash:" : tx_hash.hex() }), 200

    except auth.AuthError as e:
        print("Error verifying Firebase ID token:", e)
        return jsonify({"error": "Unauthorized"}), 403
