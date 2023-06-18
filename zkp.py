import json
import tempfile

def write_to_tmp_file(data):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, dir='/tmp') as temp_file:
        temp_file.write(json.dumps(data, indent=4))
        temp_file.flush()
        temp_file_absolute_path = '/tmp' + temp_file.name
    return temp_file_absolute_path

def generate_proof(voter_pk:str, r:str, issuer_pk, signed_commitment):
    # Create a tmp file to store the input for the ZK circuit.
    zkp_input = {
        "voter_PK": voter_pk,
        "voter_r": r,
        "enabled": "1", # Always 1
        # Public key of the issuer
        "Ax": issuer_pk[0],
        "Ay": issuer_pk[1],
        # Signed commitment using sk_issuer
        "S":signed_commitment.S,
        "R8x":signed_commitment.R[0],
        "R8y":signed_commitment.R[1],
    }
    input_file_path = write_to_tmp_file(zkp_input)

    witness_file = tempfile.NamedTemporaryFile(delete=False, dir='/tmp')
    witness_file.close()

    command = [
            "node",
            "./voting_check_js/generate_witness.js",
            "./voting_check_js/voting_check.wasm",
            input_file_path,
            '/tmp' + witness_file.name,
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
            "prove"
            "./voting/voting_check.zkey",
            "/tmp" + witness_file.name,
            "/tmp" + proof_file.name,
            "/tmp" + public_file.name,
    ]
    completed = subprocess.run(
        command,
        text=True,
        capture_output=True,
        )

    proof_file_contents = open('/tmp' + proof_file.name, 'r').read()
    public_file_contents = open('/tmp' + public_file.name, 'r').read()

    proof = json.loads(proof_file_contents)
    public = json.loads(public_file_contents)

    return (proof, public)
