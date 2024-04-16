from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract, fund_with_link, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import AdvancedCollectible, config, network
from web3 import Web3

gas_price = 20 * 10**9


def create_collectible(gas_price):
    account = get_account()
    tx_params = {"from": account}
    if gas_price:
        tx_params["gas_price"] = gas_price
    advanced_collectible = AdvancedCollectible[-1]
    
    #fund_with_link(contract_address = advanced_collectible.address, amount = Web3.toWei(0.1, "ether"), gas_price = gas_price)
    creation_tx = advanced_collectible.createCollectible(tx_params)
    creation_tx.wait(1)
    print("Print Collectible created")


def main():
    gas_price = None
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        gas_price = 20 * 10**9
    create_collectible(gas_price)