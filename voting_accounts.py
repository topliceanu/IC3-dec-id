from typing import Dict

from eth_account import Account
import web3 as w3

from vote_signature import gen_key

# 'address' : 'private_key'
accounts = {
    '0x644A0b8c42647AaEb7733cB69e792925325b1f30': '0x5e5a33688c0220a2227b0b2a878cbd7419250d94e4eb02bd4b5af0bd158c41e2',
    '0x37f4c170e34B565D655C70793eAf21B71C06a33d': '0xa6bc95777e55effec043f693118dd6099452c5d85d5e6bae9f961874e5e78a77',
    '0x28e17e23DFd9a9E85A1438e9056DfeA6888B9f63': '0xe48cf747e9b5add7dd343196e1b35ecac2e628aa52135e3a8e9bed21c1994de8',
    '0x6B276e1B9889E3E28153Dbd44305a43616927ce0': '0xb8acb18b69da6b5b06e24892f33389d4b895bae5d1699fa366dea6ca270d4b4c',
    '0x3E9116a3383218B43Aca601Cda248024574d6c57': '0xa8c33599485318db5a95ef91500c8a9ca43c690c3acd14acf07845b5b369c257',
    '0x75FC09F1B92d69DDB8236e40dD8e3191ee04b051': '0xf7f5522289ae0bc1ff65a6550a62c473462b29d5082c08cf1f2ede22daf24b07',
    '0x20eBBaeA260cB2F3635e13d52F1233536831A4d7': '0x490ce5a90bd6831be2a545ca9205b222b4c17eba80676249c1d8c43fb562251a',
    '0x04E5EaEf32D709ac19cec6832e6eA0D6B574Cbbb': '0x4a89df56dae017bc97f60e47d3eae7068d60d6857ca801f63aa4269bfedfc2a6',
    '0x501721D88872779bf6c44529Ef58fD78d823a198': '0xd8ba7e27d044c1f5f08dcb9732583a6aad462edf81cb4e096ca9e417e3268374',
    '0xBC300e8A6611EA4B2e788fDafa4fdBd6880ff6A4': '0xa5c9a0a7e68c24ccef43994c26f372ccca2ab4299ce5267f4003acdd00b13b5b'
}

def create_accounts(num_of_accounts: int) -> Dict[str, str]:
    accounts = {}
    for i in range(num_of_accounts):
        private_key, public_key, acct_address = gen_key()
        accounts[acct_address] = private_key
    return accounts

def fund_account(fund_from: str, address: str, ether_amount: float) -> str:
    # Setup infura project ID and endpoint
    infura_url = INFURA_URL

    # Connect to the Ethereum blockchain using Infura
    w3provider = w3.Web3(w3.HTTPProvider(infura_url))

    # Set the private key of the account that will vote
    my_account = Account.from_key(fund_from)
    w3provider.eth.default_account = my_account.address

    # Amount to send (in Wei, for example this is 0.01 Ether)
    amount = w3provider.to_wei(ether_amount, 'ether')

    # Build a transaction
    tx = {
        'nonce': w3provider.eth.get_transaction_count(my_account.address),
        'to': address,
        'value': amount,
        'gas': 21000,
        'gasPrice': w3provider.eth.gas_price,
    }

    # Sign the transaction
    signed_tx = w3provider.eth.account.sign_transaction(tx, fund_from)

    # Send the transaction
    tx_hash = w3provider.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = w3provider.eth.wait_for_transaction_receipt(tx_hash, 120)

    return tx_receipt['transactionHash']



if __name__ == '__main__':
    # accounts = create_accounts(10)
    # print(accounts)

    deployment_private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
    for account in accounts:
        tx_hash = fund_account(deployment_private_key, account, 0.001)
        print(tx_hash.hex())
