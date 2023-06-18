import json
import subprocess
import requests
from generate_sig import generate_keys, mimc_signature
from flask import Flask, request
from flask_cors import CORS
from attestation_check import is_attestation_valid
from vote_signature import gen_key
from generate_commitment import mimc_commit
from eth_keys import keys

app = Flask(__name__)
CORS(app)

DISCORD_SERVER_ID = "1117987715179348009"
SERVER_URL = "http://localhost:8000"

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

account_usage_mapping = {
    '0x644A0b8c42647AaEb7733cB69e792925325b1f30': False,
    '0x37f4c170e34B565D655C70793eAf21B71C06a33d': False,
    '0x28e17e23DFd9a9E85A1438e9056DfeA6888B9f63': False,
    '0x6B276e1B9889E3E28153Dbd44305a43616927ce0': False,
    '0x3E9116a3383218B43Aca601Cda248024574d6c57': False,
    '0x75FC09F1B92d69DDB8236e40dD8e3191ee04b051': False,
    '0x20eBBaeA260cB2F3635e13d52F1233536831A4d7': False,
    '0x04E5EaEf32D709ac19cec6832e6eA0D6B574Cbbb': False,
    '0x501721D88872779bf6c44529Ef58fD78d823a198': False,
    '0xBC300e8A6611EA4B2e788fDafa4fdBd6880ff6A4': False
}

# schema for users
# identifier key is the auth_token from the browser
# for each user, we have:
# public key = "pk"
# private key = "sk"
# commitment = "commitment"
# signed_commitment = "signed_commitment"
# random value for commitment = "r"
# proof = "proof"
# user's ethereum address = "voting_account"
users = {}

def get_user_eth_address(token) -> str:
    for k,v in account_usage_mapping.items():
        if v == False:
            account_usage_mapping[k] = True
            return k
    
    return "too many users have registered"

def set_user_data(token, dict_key, data):
    users[token][dict_key] = data

# deco configs
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

# issuer config
issuer_sk, issuer_pk = generate_keys(True) # make random=True

@app.route("/issue", methods = ["POST"])
def issue():
    data = request.get_json()
    attestation, commitment = data['attestation'], data['commitment']

    # run attestation check
    if not is_attestation_valid(attestation):
        return  '{"error": "deco attestation signature check failed"}', 400, { "Content-Type": "application/json" }

    # typecheck commitment

    # sign commitment
    signed_commitment = mimc_signature(commitment, issuer_sk, issuer_pk)
    print("signed commitment on the server", signed_commitment)

    payload = {
        "success": "true", 
        "data": {
            "signed_commitment": signed_commitment
        }
    }

    return json.dumps(payload), 200, { "Content-Type": "application/json" }

@app.route("/register", methods = ["POST"])
def register():
    data = request.get_json()
    print("at register route, data sent: ", data)

    auth_token = data['token']
    deco_cfg = get_deco_config(token = auth_token, server_id = DISCORD_SERVER_ID)

    serialized_cfg = json.dumps(deco_cfg)
    # private_key, public_key, acct_address = gen_key() # not in use because we have generated accounts with money now


    # attestation = subprocess.check_output(command, serialized_cfg, text=True)
    # completed = subprocess.run(
    #     command,
    #     input=serialized_cfg,
    #     text=True,
    #     capture_output=True,
    #     # stdout=subprocess.PIPE,
    #     # Pipes stderr to stdout.
    #     # stderr=subprocess.STDOUT,
    # )
    #
    # # should handle this request in a different manner
    # if completed.returncode !=0:
    #     print(completed.stderr)
    #     exit(1)
    #
    # output = completed.stdout.split('\n')
    # attestation = output[-2]


    attestation = '{"signature_scheme":"ed25519","attestation_scheme":"json","data_hex":"0x7b2273756363657373223a5b747275652c747275655d2c2270726f6f665f7370656373223a5b7b22746c735f76657273696f6e223a2276312e33222c22636c69656e74223a7b226d6574686f64223a227665726966792d72657175657374222c22726571756573745f73706563223a7b226d6574686f64223a22474554222c227075626c69635f75726c223a2268747470733a2f2f646973636f72642e636f6d2f6170692f7631302f75736572732f406d652f6775696c6473222c227365637265745f6865616465725f76616c73223a7b22417574686f72697a6174696f6e223a5b22426561726572206a7566435a77765333474553396159624a61747776344750487a6f63376a225d7d7d7d2c22736572766572223a7b226d6574686f64223a227665726966792d6a736f6e2d726573706f6e7365222c226a736f6e5f70726f6f665f73706563223a7b227061645f736563726574735f746f5f646967697473223a7b2264656661756c745f6368617273223a36347d2c2270726564696361746573223a5b7b226f70223a22696e636c75646573416e794f66222c227175657279223a222e5b5d2e6964222c227075626c69635f6f706572616e6473223a5b2231313137393837373135313739333438303039225d7d5d2c226d657461646174615f6669656c645f7061746873223a5b5d2c227075626c69635f6669656c645f7061746873223a222e5b5d2e6e616d652c2e5b5d2e69636f6e2c2e5b5d2e6f776e6572227d7d7d5d2c227075626c69635f696e70757473223a7b7d2c227075626c69635f6f757470757473223a5b5d2c2270726f7665725f63686f73656e5f61747465737465645f64617461223a22227d0a","signature_hex":"0xa4aefeb8a22c3ccc505958cdb5bec41b2e79d6bdf55743c81b8e0f1096cf808969fe3e182c03cbee199fb81e5816f94e297c50ea74264b8b76ff1b53612e9a07","public_key_hex":"0xbc8ef6058045ca7f8360b96c22ec0b55d9cc864fc2d51a84edbcfeb8531cd280"}'
    attestation = json.loads(attestation)
    # check attestation
    if not is_attestation_valid(attestation):
        exit(1)

    # register user in our internal data mapping
    users[auth_token] = {}
    eth_address = get_user_eth_address(auth_token)
    private_key = accounts[eth_address]
    public_key = keys.PrivateKey(bytes.fromhex(private_key[2:])).public_key

    set_user_data(auth_token, "voting_account", eth_address) # set voting account
    set_user_data(auth_token, "pk", public_key) # set public key
    set_user_data(auth_token, "sk", private_key) # set private key


    # make commitment
    acct_address = eth_address 
    commitment, r = mimc_commit(int(acct_address, 16))

    print("Contacting server at", SERVER_URL + "/issue")
    server_req = requests.post(SERVER_URL + "/issue", json={ "commitment": commitment, "attestation": attestation })
    print(f"Status Code: {server_req.status_code}, Response: {server_req.json()}")

    print(server_req.json()['data']['signed_commitment'])

    signed_commitment = server_req.json()['data']['signed_commitment'] 

    set_user_data(auth_token, "commitment", commitment) # set user commitment
    set_user_data(auth_token, "signed_commitment", signed_commitment) # set signed commitment
    set_user_data(auth_token, "r", r) # set random value

    payload = {
        "success": "true",
        "data": {
            "commitment": commitment,
            "public_key": str(public_key),
            "attestation": attestation,
        }
    }

    print("\n user has been loaded on the server")
    print(users[auth_token])

    # ask issuer to verify attestation, commitment, and zkp
    return json.dumps(payload), 200, { "Content-Type": "application/json" }

@app.route("/test")
def register_voter():
    return json.dumps("<h1>hello</h1>"), 200

@app.route("/vote", methods = ["POST"])
def vote():
    data = request.get_json()
    vote = data['vote']

# @app.route("/post/vote")
# def vote():
#     pass
