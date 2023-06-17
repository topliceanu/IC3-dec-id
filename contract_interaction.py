import web3 as w3


def get_contract(contract_address: str) -> w3.eth.Contract:
    # Setup infura project ID and endpoint
    infura_url = "https://goerli.infura.io/v3/a342124bc854400c8e812ca793ebc06c"

    # Connect to the Ethereum blockchain using Infura
    w3provider = w3.Web3(w3.HTTPProvider(infura_url))

    with open('Voting.abi', 'r') as f:
        contract_abi = f.read()

    # Instantiate the contract
    # noinspection PyTypeChecker
    return w3provider.eth.contract(address=contract_address, abi=contract_abi)

def get_winner(contract_address: str) -> int:
    contract = get_contract(contract_address)
    result = contract.functions.getWinningOption().call()

    print(f'Winner: {result}')
    return result

def get_votes(contract_address: str, option: int) -> int:
    contract = get_contract(contract_address)
    result = contract.functions.getVoteCount(option).call()

    print(f'Number of votes for {option}: {result}')
    return result


if __name__ == '__main__':
    contract_address = '0xb6a6a7EF95d9419eca96d2f2b8cE71D5820E59e1'
    get_votes(contract_address, 0)
    get_votes(contract_address, 1)
    get_winner(contract_address)
