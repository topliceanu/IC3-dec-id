import json

from web3 import Web3, HTTPProvider
from eth_account import Account

# Setup infura project ID and endpoint
infura_url = "https://goerli.infura.io/v3/a342124bc854400c8e812ca793ebc06c"

# Connect to the Ethereum blockchain using Infura
w3 = Web3(HTTPProvider(infura_url))

# Set the private key of the account that will vote
private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
my_account = Account.from_key(private_key)
w3.eth.default_account = my_account.address

# Define the contract address (this should be the deployed contract address)
contract_address = '0x425602Fd6D2a646EB748F78B8aeaad51Db492597'

with open('Voting.abi', 'r') as f:
    contract_abi = json.load(f)

# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Define the option that the user wants to vote for
option = 0

# Convert the option to bytes and hash it
option_bytes = option.to_bytes(32, byteorder='big')
option_hash = w3.solidity_keccak(['bytes32'], [option_bytes])

# Sign the hash
signed_message = Account.sign_hash(option_hash, private_key=private_key)

# Concatenate the r, s, and v components of the signature into a single 65-byte signature
signature = signed_message.r + signed_message.s + signed_message.v.to_bytes(1, 'big')

# Invoke the vote function
tx = contract.functions.vote(option, w3.eth.default_account, signature).buildTransaction({
    'gas': 70000,  # You may need to adjust this gas limit
    'nonce': w3.eth.get_transaction_count(w3.eth.default_account)
})

# Sign the transaction
signed_tx = w3.eth.account.signTransaction(tx, private_key)

# Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

# Wait for the transaction to be mined
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print('Transaction receipt:', tx_receipt)
