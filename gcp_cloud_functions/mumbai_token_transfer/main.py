import json
from web3 import Web3
from decimal import Decimal, getcontext

import firebase_admin
from firebase_admin import credentials, auth, firestore
from google.cloud import storage

from flask import request, jsonify

import tempfile # transform Firebase SDK key file
import functions_framework #  Enable CORS


# Read the ABI data from GLCToken.json
with open('GLCToken.json', 'r') as file:
    contract_data = json.load(file)

# Set the precision for decimal calculations (adjust this based on your requirements)
getcontext().prec = 28


# Set up the Polygon (Mumbai) network
polygon_rpc_url = "https://rpc-mumbai.maticvigil.com"  # Replace with the appropriate RPC endpoint
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Replace with test data is needed
# In Production verison this data is queried from Firebase via id_token
private_key = ""
wallet_address = ""

@functions_framework.http

def token_transfer(request):

    # Set CORS headers for the preflight request
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

    # Get the Firebase ID token from the Authorization header
    bearer_token = request.headers.get("Authorization")
    if not bearer_token:
        return jsonify({"error": "Authorization token not found"}), 401

    id_token = bearer_token.split(" ")[1]       
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

        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)

        # Access user information from the decoded token
        uid = decoded_token["uid"]
        email = decoded_token["email"]

        print(email + ' is authenticated with uid ' + uid)

        # Retrieve the user's document from the Firestore
        user_doc_ref = db.collection('users').document(uid)
        user_doc = user_doc_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            private_key = user_data.get('privateKey')
            wallet_address = user_data.get('address')
            username = user_data.get('name')
            print(username +'`s wallet is ' +wallet_address ) 

            if private_key:
                # Use the private_key
                print(f"Private Key: {private_key}")
            else:
                print("Private Key not found in user document")
        else:
            print("User document not found")

    except auth.ExpiredIdTokenError as e:
        return jsonify({"error": "Token expired"}), 401, headers

    except Exception as e:
        print("Firebase Error:", e)

    try:
        #####################################
        # Cloud Function logic start

        # GLC Token contract address
        token_contract_address = "0x7A57269A63F37244c09742d765B18b1852078072"


        # Load the contract ABI (Replace this with the actual ABI of your token contract)
        token_abi = contract_data['abi']  # Put your token contract ABI here

        # Instantiate the contract
        contract = w3.eth.contract(address=token_contract_address, abi=token_abi)

        
        # request_json = json.loads(request)
        
        request_json = request.get_json()

        if 'transactions' in request_json:
            transactions = request_json['transactions']
            results = []

            # Get the current nonce for the wallet address
            current_nonce = w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_address))


            for tx in transactions:
                to_address = tx['to_address']
                amount = Decimal(tx['amount']) # Convert the amount to a Decimal

                # Replace with the token decimals (usually 18 for most ERC20 tokens)
                token_decimals = 18

                # Convert the amount to the token's base unit
                amount_in_base_unit = int(amount * 10**token_decimals)

                # Transfer tokens
                transaction = contract.functions.transfer(to_address, amount_in_base_unit).buildTransaction({
                    'chainId': 80001,  # Replace with the appropriate chain ID (Mumbai network has chain ID 80001)
                    'gas': 200000,
                    'gasPrice': Web3.toWei('10', 'gwei'),  # Use Web3.toWei function directly
                    'nonce': current_nonce  # FOR SINGLE TRANSACTION USE: w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_address))
                    # 'value': 0,  # Set the value to 0 for ERC20 token transfers
                    })
                
                # Sign the transaction
                signed_transaction = w3.eth.account.signTransaction(transaction, private_key)

                # Send the transaction
                tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

                results.append({'to_address': to_address, 'amount': amount, 'tx_hash': tx_hash.hex()})

                # Increment the current nonce for the next transaction
                current_nonce += 1

            return jsonify(results), 200, headers

            # return jsonify(f'Transaction sent. Transaction hash: {tx_hash.hex()}'), 200, headers

        # Cloud Function logic end
        #####################################

    except json.JSONDecodeError:
        return 'Invalid JSON payload.'

    except KeyError:
        return 'Invalid request. Please provide "to_address" and "amount" in the JSON payload.'
