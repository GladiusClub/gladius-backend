from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from brownie import network
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time

def test_can_create_advanced_collectible_integration():
    #ARRANGE
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Only for integration testing")
        pytest.skip()
    gas_price = None
    tx_params = {"from": get_account(), "gas_price" : gas_price}
    #ACT
    advanced_collectible, creating_tx = deploy_and_create(gas_price)
    time.sleep(60)
    #ASSERT
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.ownerOf(0) == get_account()
