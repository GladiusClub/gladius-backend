from brownie import network, accounts, Wei

def main():
    # network.connect('polygon-test')
    # sender = accounts[0]
    sender = accounts.load('deployment_account')
    receiver = '0xD0CB7D70e1a3944bb24657AE5bc131f5b62aF0eA'  # accounts[1]
    amount = Wei("0.1 ether")

    tx = sender.transfer(receiver, amount)
    tx.wait(1)  # Wait for the transaction to be mined
    print("Transaction hash:", tx.txid)
