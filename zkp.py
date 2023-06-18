import json
import tempfile
import subprocess

def write_to_tmp_file(data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir='/tmp') as temp_file:
        temp_file.write(json.dumps(data, indent=4))
        temp_file.flush()
    return temp_file.name

def generate_proof(voter_pk, eth_address, r:str, issuer_pk, signed_commitment, commitment):
    # Create a tmp file to store the input for the ZK circuit.
    zkp_input = {
        "voter_PK": str(int(eth_address, 16)),
        #"voter_PK": str(int.from_bytes(voter_pk.to_bytes(), byteorder="big")),
        "voter_r": str(r),
        "enabled": "1", # Always 1
        # Public key of the issuer
        "Ax": str(issuer_pk[0]),
        "Ay": str(issuer_pk[1]),
        # Signed commitment using sk_issuer
        "S":str(signed_commitment[1]),
        "R8x":str(signed_commitment[0][0]),
        "R8y":str(signed_commitment[0][1]),
        # Commitment
        "M": str(commitment),
    }
    input_file_path = write_to_tmp_file(zkp_input)

    witness_file = tempfile.NamedTemporaryFile(delete=False, dir='/tmp')
    witness_file.close()

    command = [
            "node",
            "./voting/voting_check_js/generate_witness.js",
            "./voting/voting_check_js/voting_check.wasm",
            input_file_path,
            witness_file.name,
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        )

    proof_file = tempfile.NamedTemporaryFile(delete=False, dir='/tmp')
    proof_file.close()

    public_file = tempfile.NamedTemporaryFile(delete=False, dir='/tmp')
    public_file.close()

    command = [
            "snarkjs",
            "groth16",
            "prove",
            "./voting/voting_check.zkey",
            witness_file.name,
            proof_file.name,
            public_file.name,
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        )

    proof_file_contents = open(proof_file.name, 'r').read()
    public_file_contents = open(public_file.name, 'r').read()

    proof = json.loads(proof_file_contents)
    public = json.loads(public_file_contents)

    return (proof, public)
