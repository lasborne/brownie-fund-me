from brownie import accounts, network, exceptions
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me
import pytest

def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    print(tx)
    tx2 = fund_me.withdraw(accounts[1], 2500000, {"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0
    print(tx2)

def test_only_owner_can_withdraw():
    if network.show_active() not in ["development", "ganache-local"]:
        pytest.skip("only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    fund_me.withdraw(accounts[2], 3, {"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw(accounts[2], 3, {"from": bad_actor})