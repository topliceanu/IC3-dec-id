import json

from web3 import Web3, HTTPProvider
from eth_account import Account

from vote_signature import sign_vote


def vote(vote: int, contract_address: str, private_key_to_sign_vote: str, public_address_to_verify_vote: str,
         private_key_to_sign_transaction: str) -> str:
    # Setup infura project ID and endpoint
    infura_url = "https://goerli.infura.io/v3/a342124bc854400c8e812ca793ebc06c"

    # Connect to the Ethereum blockchain using Infura
    w3 = Web3(HTTPProvider(infura_url))

    # Set the private key of the account that will vote
    my_account = Account.from_key(private_key_to_sign_transaction)
    w3.eth.default_account = my_account.address

    with open('Voting.abi', 'r') as f:
        contract_abi = f.read()

    # Instantiate the contract
    # noinspection PyTypeChecker
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Sign the hash
    vote_signature = sign_vote(vote, private_key_to_sign_vote)

    # Build the transaction
    vote_func = contract.functions.vote(vote, public_address_to_verify_vote, vote_signature)
    gas_estimate = vote_func.estimate_gas()

    # Invoke the vote function
    tx = vote_func.build_transaction({
        'gas': gas_estimate,
        'nonce': w3.eth.get_transaction_count(w3.eth.default_account)
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key_to_sign_transaction)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 60)

    return tx_receipt['transactionHash']


if __name__ == '__main__':
    from vote_signature import gen_key
    private_key_to_sign_vote, _, public_address_to_verify_vote = gen_key()

    from deploy import deploy_contract
    contract_address = deploy_contract()
    print(f'Contract deployed at: {contract_address}')
    # contract_address = '0xb6a6a7EF95d9419eca96d2f2b8cE71D5820E59e1'

    deployment_private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
    transaction_hash = vote(0, contract_address, private_key_to_sign_vote, public_address_to_verify_vote,
                            deployment_private_key)

    print(f'Transaction hash: {transaction_hash}')
