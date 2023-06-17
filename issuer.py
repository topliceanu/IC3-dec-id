import pprint
import json
from flask import Flask, request

app = Flask(__name__)

def is_attestation_valid(attestation) -> bool:

    try:
        pub_key_bytes = bytes.fromhex(attestation['public_key_hex'][2:])
        sig_bytes = bytes.fromhex(attestation['signature_hex'][2:])
        msg_bytes = bytes.fromhex(attestation['data_hex'][2:])

        verify_key = VerifyKey(pub_key_bytes) # public key

        verify_key.verify(msg_bytes, sig_bytes)
        print("Server attestation has been verified.")
        return True
    except:
        print("Server attestation verification has failed.")
        return False

@app.route("/issue", methods = ["POST"])
def issue():
    print('hello')
    data = request.get_json()
    print("received data from user", pprint.pprint(data))
    attestation, commitment = data['attestation'], data['commitment']

    print("received attestation", attestation)
    print()
    print("received commitment", commitment)
    print()

    # run attestation check
    if not is_attestation_valid(attestation):
        return  '{"error": "deco attestation signature check failed"}', 400, { "Content-Type": "application/json" }

    # typecheck commitment

    return "success", 200 

# @app.route("/post/register")
# def register_voter():
#     pass
#
# @app.route("/post/vote")
# def vote():
#     pass
