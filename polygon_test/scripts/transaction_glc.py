from brownie import accounts, GLCToken

def main():
    account = accounts.load('deployment_account')

    receiver = '0xD0CB7D70e1a3944bb24657AE5bc131f5b62aF0eA' 

    amount = 1 * 10**18

    token = GLCToken.deploy(amount, {'from': account})

    token.mint(account, amount, {'from': account})

    token.transfer(receiver, amount, {'from': account})


    print("Tokens transferred successfully!")
