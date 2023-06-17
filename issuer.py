import json
from generate_sig import generate_keys, mimc_signature
from flask import Flask, request

from attestation_check import is_attestation_valid

app = Flask(__name__)

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
            "commitment": commitment
        }
    }

    return json.dumps(payload), 200, { "Content-Type": "application/json" }

# @app.route("/post/register")
# def register_voter():
#     pass
#
# @app.route("/post/vote")
# def vote():
#     pass
