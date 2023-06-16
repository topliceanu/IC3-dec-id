import subprocess
import json
from nacl.signing import VerifyKey

command = [
    "docker",
    "run",
    "-i",
    "--rm",
    "-e",
    "GOLOG_LOG_LEVEL=info",
    "--network=host",
    "deco:v0.8.1-rc2"
]

def get_deco_config(token, server_id):
    return {
  "mode": "prover",
  "prover": {
    "verifier_addr": "http://api.deco.works:12345",
    "num_zkp_threads": 4,
    "signature_scheme": "ed25519",
    "attestation_scheme": "json",
    "auth": "005a587151514a45313338676f6f4e6547334c4157356c4c39795732526a7a41"
  },
  "proof_specs": [
    {
      "tls_version": "v1.3",
      "client": {
        "method": "verify-request",
        "request_spec": {
          "method": "GET",
          "public_url": "https://discord.com/api/v10/users/@me/guilds",
          "secret_header_vals": {
            "Authorization": [
              token
            ]
          }
        }
      },
      "server": {
        "method": "verify-json-response",
        "json_proof_spec": {
          "pad_secrets_to_digits": {
            "default_chars": 64
          },
          "predicates": [
            {
              "op": "includesAnyOf",
              "query": ".[].id",
              "public_operands": [
                server_id
              ]
            }
          ],
          "metadata_field_paths": [],
          "public_field_paths": ".[].name,.[].icon,.[].owner"
        }
      }
    }
  ]
}

def is_attestation_valid(attestation) -> bool:

    try:
        pub_key_bytes = bytes.fromhex(attestation['public_key_hex'][2:])
        sig_bytes = bytes.fromhex(attestation['signature_hex'][2:])
        msg_bytes = bytes.fromhex(attestation['data_hex'][2:])

        verify_key = VerifyKey(pub_key_bytes) # public key

        verify_key.verify(msg_bytes, sig_bytes)
        print("Attestation has been verified.")
        return True
    except:
        print("Attestation verification has failed.")
        return False


if __name__ == "__main__":
    auth_token = "Bearer jufCZwvS3GES9aYbJatwv4GPHzoc7j" # sys.argv[1]
    deco_cfg = get_deco_config(token = auth_token, server_id = "1117987715179348009")
    serialized_cfg = json.dumps(deco_cfg)

    #print(serialized_cfg)
    #attestation = subprocess.check_output(command, serialized_cfg, text=True)
    #completed = subprocess.run(
    #    command,
    #    input=serialized_cfg,
    #    text=True,
    #    capture_output=True,
    #    # stdout=subprocess.PIPE,
    #    # Pipes stderr to stdout.
    #    # stderr=subprocess.STDOUT,
    #)
    #if completed.returncode !=0:
    #    print(completed.stderr)
    #    exit(1)

    #output = completed.stdout.split('\n')
    #attestation = output[-2]
    attestation = '{"signature_scheme":"ed25519","attestation_scheme":"json","data_hex":"0x7b2273756363657373223a5b747275652c747275655d2c2270726f6f665f7370656373223a5b7b22746c735f76657273696f6e223a2276312e33222c22636c69656e74223a7b226d6574686f64223a227665726966792d72657175657374222c22726571756573745f73706563223a7b226d6574686f64223a22474554222c227075626c69635f75726c223a2268747470733a2f2f646973636f72642e636f6d2f6170692f7631302f75736572732f406d652f6775696c6473222c227365637265745f6865616465725f76616c73223a7b22417574686f72697a6174696f6e223a5b22426561726572206a7566435a77765333474553396159624a61747776344750487a6f63376a225d7d7d7d2c22736572766572223a7b226d6574686f64223a227665726966792d6a736f6e2d726573706f6e7365222c226a736f6e5f70726f6f665f73706563223a7b227061645f736563726574735f746f5f646967697473223a7b2264656661756c745f6368617273223a36347d2c2270726564696361746573223a5b7b226f70223a22696e636c75646573416e794f66222c227175657279223a222e5b5d2e6964222c227075626c69635f6f706572616e6473223a5b2231313137393837373135313739333438303039225d7d5d2c226d657461646174615f6669656c645f7061746873223a5b5d2c227075626c69635f6669656c645f7061746873223a222e5b5d2e6e616d652c2e5b5d2e69636f6e2c2e5b5d2e6f776e6572227d7d7d5d2c227075626c69635f696e70757473223a7b7d2c227075626c69635f6f757470757473223a5b5d2c2270726f7665725f63686f73656e5f61747465737465645f64617461223a22227d0a","signature_hex":"0xa4aefeb8a22c3ccc505958cdb5bec41b2e79d6bdf55743c81b8e0f1096cf808969fe3e182c03cbee199fb81e5816f94e297c50ea74264b8b76ff1b53612e9a07","public_key_hex":"0xbc8ef6058045ca7f8360b96c22ec0b55d9cc864fc2d51a84edbcfeb8531cd280"}'
    attestation = json.loads(attestation)

    # check attestation
    if not is_attestation_valid(attestation):
        exit(1)

    # make commitment

    # make zkp

    # ask issuer to verify attestation, commitment, and zkp
