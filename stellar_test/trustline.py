# example
# https://stellar.expert/explorer/testnet/tx/1556345824223232

from stellar_sdk import Server, Keypair, Network, TransactionBuilder, Asset

# Use testnet for testing or development purposes
server = Server("https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# Assuming you have the secret keys for both accounts
#issuer_secret = ''
trustor_secret = ''

#issuer_keypair = Keypair.from_secret(issuer_secret)
trustor_keypair = Keypair.from_secret(trustor_secret)

#issuer_account = server.load_account(account_id=issuer_address)
trustor_account = server.load_account(account_id=trustor_keypair.public_key)

issuer_address ='GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY'

# Define the asset
asset_code = "EURC"
asset = Asset(asset_code, issuer_address)

# Start building the transaction
transaction = (
    TransactionBuilder(
        source_account=trustor_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_change_trust_op(asset=asset, limit="1000000")  # You can adjust the limit
    .set_timeout(30)
    .build()
)

# Sign the transaction with the trustor's secret key
transaction.sign(trustor_keypair)

# Finally, submit the transaction to the Stellar network
response = server.submit_transaction(transaction)
print(f"Transaction hash: {response['hash']}")
