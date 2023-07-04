from brownie import accounts, GLCToken

def main():
    sender = '0x717320e0Ea465dD9ee7b0345219DB1A6b2884869'
    receiver = '0xD0CB7D70e1a3944bb24657AE5bc131f5b62aF0eA' #accounts[1]
    amount = 0.1  # Amount of GLC tokens to transfer

    # Get the deployed contract address
    glc_token_address = "0x7E049b105Ab7b916bF8D0a4111b25ff4bA94758C"  # Replace with the actual contract address

    # Create a contract instance using the address
    glc_token = GLCToken.at(glc_token_address)

    # Transfer the GLC tokens from the sender to the receiver
    glc_token.transfer(receiver, amount * 10**18, {'from': sender})

    print("Transfer successful!")