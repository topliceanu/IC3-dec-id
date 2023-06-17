import json
from flask import Flask, request

from attestation_check import is_attestation_valid

app = Flask(__name__)

@app.route("/issue", methods = ["POST"])
def issue():
    data = request.get_json()
    attestation, commitment = data['attestation'], data['commitment']

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
