import json
from web3 import Web3
from decimal import Decimal, getcontext

import firebase_admin
from firebase_admin import credentials, auth
from google.cloud import storage

#from flask import request, jsonify
from flask import Flask, request, jsonify
from main import token_transfer

import tempfile

app = Flask(__name__)

@app.route('/transfer', methods=['POST'])

def transfer_endpoint():
    result = token_transfer(request)
    return result

# Read the ABI data from GLCToken.json
with open('GLCToken.json', 'r') as file:
    contract_data = json.load(file)

# Set the precision for decimal calculations (adjust this based on your requirements)
getcontext().prec = 28

# Set up the Polygon (Mumbai) network
polygon_rpc_url = "https://rpc-mumbai.maticvigil.com"  # Replace with the appropriate RPC endpoint
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Replace these variables with your actual values
private_key = '0xef9d1a761a291eea5e37529ff89030bc745d87e01e94039efe56ee6e681bcd5b'
wallet_address = '0x717320e0Ea465dD9ee7b0345219DB1A6b2884869'

# Create a mock request object with headers and data
class MockRequest:
    def __init__(self, authorization, data):
        self.headers = {'Authorization': authorization}
        self.data = data


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

        print(credentials_file_path + ' was downloaded from ' + bucket_name)

        # Initialize the Firebase Admin SDK with the downloaded service account credentials
        #cred = credentials.Certificate(credentials_file_content)
                
        # Create a temporary file to write the credentials content
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(credentials_file_content.encode())
            temp_file_path = temp_file.name

        # Initialize the Firebase Admin SDK with the temporary file
        cred = credentials.Certificate(temp_file_path)
        firebase_admin.initialize_app(cred)


        print('Firebase connection is up')

        # If the above doesn't work:
        # Create a temporary file and write the content of the credentials JSON to it
        # with open("/tmp/serviceAccountKey.json", "w") as tmp_file:
        #    tmp_file.write(credentials_file_content)

        # Initialize the Firebase Admin SDK with the downloaded service account credentials
        #cred = credentials.Certificate("/tmp/serviceAccountKey.json")
        #firebase_admin.initialize_app(cred)

    except Exception as e:
            print("Error initializing Firebase Admin SDK:", e)

def generate_custom_token(uid):
    
    custom_token = auth.create_custom_token(uid)
    return custom_token


# Function to transfer tokens
def token_transfer(request):
    # Get the Firebase ID token from the Authorization header
    bearer_token = request.headers.get("Authorization")
    if not bearer_token:
        return jsonify({"error": "Authorization token not found"}), 401

    id_token = bearer_token.split(" ")[1]      

    # Call this function to initialize the Firebase Admin SDK in your Cloud Function
    #initialize_firebase_admin_sdk()

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)

        # Access user information from the decoded token
        uid = decoded_token["uid"]
        email = decoded_token["email"]
        # Add any other user-related data you need

        print(email + ' is authenticated')

        #####################################
        # Cloud Function logic start

        #Cloud Function 
        #request_json = json.loads(request)  # Deserialize the JSON string to a dictionary

        #Test
        request_json = request.get_json()  # Access the JSON payload directly from the request dictionary
        

        if 'to_address' in request_json and 'amount' in request_json:

            to_address = request_json['to_address']
            amount = Decimal(request_json['amount'])  # Convert the amount to a Decimal

            # GLC Token contract address
            token_contract_address = "0x7A57269A63F37244c09742d765B18b1852078072"

            # Replace with the token decimals (usually 18 for most ERC20 tokens)
            token_decimals = 18

            # Convert the amount to the token's base unit
            amount_in_base_unit = int(amount * 10**token_decimals)

            # Load the contract ABI (Replace this with the actual ABI of your token contract)
            token_abi = contract_data['abi']  # Put your token contract ABI here

            # Instantiate the contract
            contract = w3.eth.contract(address=token_contract_address, abi=token_abi)

            
            # Check if the request is for a mint or transfer operation
            if 'mint' in request_json and request_json['mint']:
                # Mint new tokens
                transaction = contract.functions.mint(to_address, amount_in_base_unit).buildTransaction({
                    'chainId': 80001,  # Replace with the appropriate chain ID (Mumbai network has chain ID 80001)
                    'gas': 200000,
                    'gasPrice': Web3.toWei('10', 'gwei'),  # Use Web3.toWei function directly
                    'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_address))
                    #'value': 0,  # Set the value to 0 for ERC20 token transfers
                })
            else:
                # Transfer tokens
                transaction = contract.functions.transfer(to_address, amount_in_base_unit).buildTransaction({
                    'chainId': 80001,  # Replace with the appropriate chain ID (Mumbai network has chain ID 80001)
                    'gas': 200000,
                    'gasPrice': Web3.toWei('10', 'gwei'),  # Use Web3.toWei function directly
                    'nonce': w3.eth.getTransactionCount(w3.toChecksumAddress(wallet_address))
                    #'value': 0,  # Set the value to 0 for ERC20 token transfers
                })


            # Sign the transaction
            signed_transaction = w3.eth.account.signTransaction(transaction, private_key)

            # Send the transaction
            tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
            

        # Cloud Function logic end
        # #####################################

            return f'Transaction sent. Transaction hash: {tx_hash.hex()}'

    except json.JSONDecodeError:
        return 'Invalid JSON payload.'

    except KeyError:
        return 'Invalid request. Please provide "to_address" and "amount" in the JSON payload.'

if __name__ == "__main__":

    # Call this function to initialize the Firebase Admin SDK in your Cloud Function
    initialize_firebase_admin_sdk()

    app.run()


    uid = '4EfgKK9FsUVL35oNKWSQ21VG5pz2' #Bob
    custom_token = auth.create_custom_token(uid)
    
    authorization = "Bearer " + custom_token
    print(authorization)

    json_payload = {
        "to_address": "0xce912F29932994e60A7aEEa9F18F7C16E086CBAc",
        "amount": "0.01",
        "mint": False  # Set to True if you want to perform a mint operation
    }
    data = json.dumps(json_payload)

    # Create a mock request
    mock_request = MockRequest(authorization, data)

    # Call the token_transfer function with the mock request
    result = token_transfer(mock_request)

    # Print the result
    print(result)
