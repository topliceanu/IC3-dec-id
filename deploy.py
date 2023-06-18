import json

from web3 import Web3, HTTPProvider
from eth_account import Account

from compile import compile_contract


def deploy_voting_contract(num_of_blocks: int = 10000) -> str:
    # Setup infura project ID and endpoint
    infura_url = "https://goerli.infura.io/v3/a342124bc854400c8e812ca793ebc06c"

    # Connect to the Ethereum blockchain using Infura
    w3 = Web3(HTTPProvider(infura_url))

    # Set the private key of the account that will vote
    private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
    my_account = Account.from_key(private_key)
    w3.eth.default_account = my_account.address

    # Define the contract ABI and bytecode (these should be the ABI and bytecode of your contract)
    contract_abi, contract_bytecode = compile_contract('Voting.sol', 'VotingContract')

    with open(f'Voting.abi', 'w') as f:
        json.dump(contract_abi, f)

    with open('issuer_keys.json') as f:
        issuer_pk = json.load(f)['issuer_pk']

    verifier_contract_address = Web3.to_checksum_address('0x8c4c43c64943a7a6fd0ab8575194afaaafbfcdf1')

    # Define the arguments for the contract constructor (if any)
    constructor_args = (num_of_blocks, issuer_pk[0],issuer_pk[1])

    # Build a transaction to deploy the contract
    contract_factory = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    contract = contract_factory.constructor(*constructor_args)

    # Estimate the gas required to deploy the contract
    gas_estimate = w3.eth.estimate_gas({
        'from': w3.eth.default_account,
        'data': contract.data_in_transaction,
        'to': None,
        'value': 0
    })

    tx = contract.build_transaction({
        'from': w3.eth.default_account,
        'nonce': w3.eth.get_transaction_count(w3.eth.default_account),
        'gas': gas_estimate,
        'gasPrice': w3.eth.gas_price,
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(tx_hash.hex())

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 60)

    address = tx_receipt['contractAddress']
    with open(f'voting_contract_address.json', 'w') as f:
        json.dump({'address': address}, f)

    return tx_receipt['contractAddress']

def deploy_verifier_contract() -> str:
    # Setup infura project ID and endpoint
    infura_url = "https://goerli.infura.io/v3/a342124bc854400c8e812ca793ebc06c"

    # Connect to the Ethereum blockchain using Infura
    w3 = Web3(HTTPProvider(infura_url))

    # Set the private key of the account that will vote
    private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
    my_account = Account.from_key(private_key)
    w3.eth.default_account = my_account.address

    # Define the contract ABI and bytecode (these should be the ABI and bytecode of your contract)
    contract_abi, contract_bytecode = compile_contract('voting_verifier.sol', 'Groth16Verifier')

    with open(f'Groth16Verifier.abi', 'w') as f:
        json.dump(contract_abi, f)


    # Build a transaction to deploy the contract
    contract_factory = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    contract = contract_factory.constructor()

    # Estimate the gas required to deploy the contract
    gas_estimate = w3.eth.estimate_gas({
        'from': w3.eth.default_account,
        'data': contract.data_in_transaction,
        'to': None,
        'value': 0
    })

    tx = contract.build_transaction({
        'from': w3.eth.default_account,
        'nonce': w3.eth.get_transaction_count(w3.eth.default_account),
        'gas': gas_estimate,
        'gasPrice': w3.eth.gas_price,
    })

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 60)

    return tx_receipt['contractAddress']

if __name__ == '__main__':
    tx = deploy_voting_contract(1000)
    print(tx)
    # deploy_verifier_contract()