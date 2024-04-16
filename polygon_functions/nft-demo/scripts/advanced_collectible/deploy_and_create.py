from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract, fund_with_link, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import AdvancedCollectible, config, network
from web3 import Web3
import os

# Create a new Web3 instance
goerli_url = f"https://goerli.infura.io/v3/{os.getenv('WEB3_INFURA_PROJECT_ID')}"
web3 = Web3(Web3.HTTPProvider(goerli_url))



def deploy_and_create():
    transaction_cost_eth = Web3.fromWei(124381747787472952, 'ether')
    print("Transaction cost in ETH:", transaction_cost_eth)

    account = get_account()
    print(account)
    tx_params = {"from": account}
    #tx_params["gas_price"] = Web3.toWei(500, "gwei") 
    ##print(tx_params["gas_price"] )
    #tx_params["gas_limit"] = Web3.toWei(8000000, "gwei")
    print("GAS PRICE: ", web3.eth.gas_price)

    gas_estimate = AdvancedCollectible.deploy.estimate_gas(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config['networks'][network.show_active()]["keyhash"],
        config['networks'][network.show_active()]["fee"],
        tx_params,
    )

    print("GAS LIMIT: ", gas_estimate)


    print("Account balance:", account.balance(), "wei")
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config['networks'][network.show_active()]["keyhash"],
        config['networks'][network.show_active()]["fee"],
        tx_params)
    fund_with_link(contract_address = advanced_collectible.address)
    
    creating_tx = advanced_collectible.createCollectible(tx_params)
    creating_tx.wait(1)
    print("Contract deployed and New token has been created")
    return advanced_collectible, creating_tx
    


def main():
    deploy_and_create()
    

