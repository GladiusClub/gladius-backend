import json
from web3 import Web3
from decimal import Decimal, getcontext

# Read the ABI data from GLCToken.json
with open('GLCToken.json', 'r') as file:
    contract_data = json.load(file)

# Set the precision for decimal calculations (adjust this based on your requirements)
getcontext().prec = 28

# Set up the Polygon (Mumbai) network
polygon_rpc_url = "https://rpc-mumbai.maticvigil.com"  # Replace with the appropriate RPC endpoint
w3 = Web3(Web3.HTTPProvider(polygon_rpc_url))

# Replace these variables with your actual values
private_key = ''
wallet_address = ''

# Function to transfer tokens
def token_transfer(request):
    try:
        #request_json = json.loads(request)  # Deserialize the JSON string to a dictionary
        request_json = request.get_json()
        if 'to_address' in request_json and 'amount' in request_json:
            to_address = request_json['to_address']
            amount = Decimal(request_json['amount'])  # Convert the amount to a Decimal

            # GLC Token contract address
            token_contract_address = ""

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

            return f'Transaction sent. Transaction hash: {tx_hash.hex()}'

    except json.JSONDecodeError:
        return 'Invalid JSON payload.'

    except KeyError:
        return 'Invalid request. Please provide "to_address" and "amount" in the JSON payload.'