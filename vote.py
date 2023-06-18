import json

from web3 import Web3, HTTPProvider
from eth_account import Account

from vote_signature import sign_vote

def vote(vote: int, contract_address: str, private_key_to_sign_vote: str, public_address_to_verify_vote: str,
         private_key_to_sign_transaction: str, proof) -> str:
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

    # Disassemble proof
    pa = [int(i) for i in proof['pi_a']][:2]
    pb = [[int(i) for i in l] for l in proof['pi_b']][:2]
    pc = [int(i) for i in proof['pi_c']][:2]

    # Build the transaction
    vote_func = contract.functions.vote(vote, public_address_to_verify_vote, vote_signature, pa, pb, pc)
    gas_estimate = vote_func.estimate_gas()

    # Invoke the vote function
    tx = vote_func.build_transaction({
        'gas': gas_estimate,
        'nonce': w3.eth.get_transaction_count(w3.eth.default_account)
    })(str,str,str)

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

    # from deploy import deploy_voting_contract
    # contract_address = deploy_voting_contract()
    # print(f'Contract deployed at: {contract_address}')
    contract_address = Web3.to_checksum_address('0x428ec0e46869c593b5293c169d7b3a0c90d523e2')

    proof = {'pi_a':
                 ['15562274451659027381878005828066679949078614184963982851792018092783121752936',
                  '15353747895582752856526166975490668935965360696251341852992775764465284965779',
                  '1'],
             'pi_b': [
                 ['13158560307247234383012396089334615587163531509983035030000058741568519584462',
                  '1961713628788634694773445487289256346440971852197075948769887893075877418001'],
                 ['13736980634187096257386794367649741829932616366035386730180280730211924626314',
                  '7858679162281078299794114983995069520075531456017678704287566329035724125281'],
                 ['1', '0']],
             'pi_c':
                 ['8171618625505424270264642261999456637791368245348073463653436089253104263097',
                  '4831115321494603611681692526569906262858634052461378299389375989353274613865',
                  '1'],
             'protocol': 'groth16', 'curve': 'bn128'}

    deployment_private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
    transaction_hash = vote(0, contract_address, private_key_to_sign_vote, public_address_to_verify_vote,
                            deployment_private_key, proof)

    print(f'Transaction hash: {transaction_hash}')
