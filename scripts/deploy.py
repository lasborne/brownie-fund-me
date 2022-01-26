
from brownie import FundMe, MockV3Aggregator, network, config

from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me():
    account = get_account()
    # Pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    tr = deploy_mocks()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
        tr = price_feed_address
    else:
        deploy_mocks()
    fund_me = FundMe.deploy(tr, {"from": account}, 
        publish_source = config["networks"][network.show_active()].get("verify"))
    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()