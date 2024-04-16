from brownie import accounts

def main():
    # my_account = accounts[0]  # Get the first account from the accounts module
    my_account = accounts.load('deployment_account')
    private_key = my_account.private_key

    print("Private Key:", private_key)
