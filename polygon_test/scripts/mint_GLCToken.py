from brownie import GLCToken, accounts

def main():
    account = accounts.load('deployment_account')
    amount = 1000000

    token = GLCToken.deploy(amount, {'from': account})


    token.mint(account, amount, {'from': account})

    print("GLC Tokens minted:", amount)
