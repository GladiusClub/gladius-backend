from brownie import GLCToken, accounts

def main():
    account = accounts.load('deployment_account')
    initial_supply = 1000000000

    glc_token = GLCToken.deploy(initial_supply, {'from': account})
    print("GLC Token deployed at address:", glc_token.address)
