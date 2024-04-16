from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible


to_address = "0xaaEd609fC131C60e072734CbE296c253256413b6"
#to_address = get_account(2)

def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(0, to_address, {"from": account})
    tx.wait(1)
    print(f"You can see the NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}")
    return simple_collectible

def main():
    deploy_and_create()