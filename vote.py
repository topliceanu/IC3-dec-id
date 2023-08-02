import json

from web3 import Web3, HTTPProvider
from eth_account import Account

from vote_signature import sign_vote

def vote(vote: int, contract_address: str, private_key_to_sign_vote: str, public_address_to_verify_vote: str,
         private_key_to_sign_transaction: str, proof) -> str:
    # Setup infura project ID and endpoint
    infura_url = INFURA_URL

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

    # Reverse the lists in pb to match the order required by the Groth16 verifier
    pb = [l[::-1] for l in pb]

    # Build the transaction
    print('Contract params',
          # Convert all ' to " and wrap all strings in " to make it valid JSON
          str((
              str(vote),
              str(Web3.to_checksum_address(public_address_to_verify_vote)),
              str(vote_signature),
              [str(v) for v in pa],
              [[str(v) for v in l] for l in pb],
              [str(v) for v in pc]
          )).replace("'", '"'))
    vote_func = contract.functions.vote(vote, Web3.to_checksum_address(public_address_to_verify_vote),
                                        vote_signature, pa, pb, pc)
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
    # from vote_signature import gen_key
    # private_key_to_sign_vote, _, public_address_to_verify_vote = gen_key()

    # from deploy import deploy_voting_contract
    # contract_address = deploy_voting_contract()
    # print(f'Contract deployed at: {contract_address}')
    contract_address = Web3.to_checksum_address('0xeb68d1Db74dF56DD2A431B0F3D1097Aa7DfAB42c')

    # proof = {'pi_a':
    #              ['15562274451659027381878005828066679949078614184963982851792018092783121752936',
    #               '15353747895582752856526166975490668935965360696251341852992775764465284965779',
    #               '1'],
    #          'pi_b': [
    #              ['13158560307247234383012396089334615587163531509983035030000058741568519584462',
    #               '1961713628788634694773445487289256346440971852197075948769887893075877418001'],
    #              ['13736980634187096257386794367649741829932616366035386730180280730211924626314',
    #               '7858679162281078299794114983995069520075531456017678704287566329035724125281'],
    #              ['1', '0']],
    #          'pi_c':
    #              ['8171618625505424270264642261999456637791368245348073463653436089253104263097',
    #               '4831115321494603611681692526569906262858634052461378299389375989353274613865',
    #               '1'],
    #          'protocol': 'groth16', 'curve': 'bn128'}

    option = 1
    contract_address = '0xeb68d1Db74dF56DD2A431B0F3D1097Aa7DfAB42c'
    private_key_to_sign_vote = '0x5e5a33688c0220a2227b0b2a878cbd7419250d94e4eb02bd4b5af0bd158c41e2'
    public_address_to_verify_vote = '0x644A0b8c42647AaEb7733cB69e792925325b1f30'
    # public_address_to_verify_vote = '0x490af7cdb889c48c07d6f8991fbff74396c62973e8540e042bb70942ad8a84456f1bcd35274a11136d4890535117a79d7da7a69957bcb2ed4b38f4d05c45314f'
    send_tx_address = '0x5e5a33688c0220a2227b0b2a878cbd7419250d94e4eb02bd4b5af0bd158c41e2'
    proof = {'pi_a': ['13697782731615823716007568340420432488392389381739985808682263232487332935842',
              '2767393836361064673459261057872505029756677364906039423551903198140103535705', '1'], 'pi_b': [
        ['17980062803951153460700313596433938874698188131787402768132129741347497063685',
         '12803869575550250845008561050034742233066936130739446995712425715427084075419'],
        ['10061832049543266518708374350079283586826369301115522885527431007157822003731',
         '4715819599298502457142598781627692566070046808063220597517046705759287029797'], ['1', '0']],
     'pi_c': ['20716001530272162660557263875964058567432966967665131986808342700370659004018',
              '1211865286496123190855980455342157474644007294939728074462639869485673131922', '1'],
     'protocol': 'groth16', 'curve': 'bn128'}

    # transaction_hash = vote(option, contract_address, private_key_to_sign_vote, public_address_to_verify_vote,
    #                         send_tx_address, proof)

    args = (
        1,
        '0x04C65a9F60963fD62Bb539618DCECf2a74A7a896',
        '0x5e5a33688c0220a2227b0b2a878cbd7419250d94e4eb02bd4b5af0bd158c41e2',
        '0x644A0b8c42647AaEb7733cB69e792925325b1f30',
        '0x5e5a33688c0220a2227b0b2a878cbd7419250d94e4eb02bd4b5af0bd158c41e2',
        {
            'pi_a':
            [
                '873001267310603190896701013382933637125916198828729124126196794054817986870',
                '17575541452019960402536467926348638972591941941483107610707119754488201147418',
                '1'
            ],
            'pi_b':
            [
                [
                    '14460593531141460946857198143374167637175174350958035873416396029278478450885',
                    '149921841923923877921576406334420611547863379255396862544383444177817882790'
                ],
                [
                    '1364587075593790675778832869636769771098892684960564824135903705267014397258',
                    '18203631379030205728400284494938879473956272412568075351932077078800648775451'
                ],
                [
                    '1',
                    '0'
                ]
            ],
            'pi_c':
                [
                    '18912844620528115999533657541458470210995329035208371062336787419867050846711',
                    '18077049637364684765893608892248591809011829519916774951660462760612425356304',
                    '1'
                ],
            'protocol':
                'groth16',
            'curve':
                'bn128'
        }
        )

    transaction_hash = vote(*args)

    # deployment_private_key = '0x9c07c5b4e3ad30f78303fc1d73eb6e269aa1753bb2f4500fa7210b876156f467'
    # transaction_hash = vote(0, contract_address, private_key_to_sign_vote, public_address_to_verify_vote,
    #                         deployment_private_key, proof)

    print(f'Transaction hash: {transaction_hash}')
