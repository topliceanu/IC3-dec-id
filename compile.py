import json

import solcx
from solcx import compile_standard, install_solc


def compile_contract(path: str, name: str):
    # Ensure that we're using the same version of Solidity that the contract expects
    version = install_solc('0.8.16')

    # Define the contract source code (replace this with your actual contract source code)
    # Here, we're reading it from a .sol file
    with open(path, 'r') as file:
        contract_source_code = file.read()

    # Define the contract compilation input
    compilation_input = {
        "language": "Solidity",
        "sources": {
            path: {
                "content": contract_source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    }

    # Compile the contract
    compilation_result = compile_standard(compilation_input, solc_version=version)

    # Get the contract ABI and bytecode
    contract_interface = compilation_result['contracts'][path][f'{name}']
    contract_bytecode = contract_interface['evm']['bytecode']['object']
    contract_abi = json.loads(contract_interface['metadata'])['output']['abi']

    return contract_abi, contract_bytecode
