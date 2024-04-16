from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from brownie import network
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible():
    #ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    gas_price = 20 * 10**9
    tx_params = {"from": get_account(), "gas_price" : gas_price}
    #ACT
    advanced_collectible, creating_tx = deploy_and_create(gas_price)
    requestId = creating_tx.events['requestedCollectible']['requestId']
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 
        random_number,
        advanced_collectible.address, 
        tx_params)
    print(advanced_collectible.tokenCounter)
    #ASSERT
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.ownerOf(0) == get_account()
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
