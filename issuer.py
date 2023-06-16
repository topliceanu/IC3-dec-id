from flask import Flask

app = Flask(__name__)

@app.route("/post/issue")
def issue():
    data = request.json
    attestation, commitment, proof = data.attestation, data.commitment, data.proof

    # run attestation check
    if not check_deco_attestation_sig(attestation):
        return  '{"error": "deco attestation signature check failed"}', status.HTTP_400_BAD_REQUEST, { Content-Type: "application/json" }

    # typecheck commitment

# @app.route("/post/register")
# def register_voter():
#     pass
#
# @app.route("/post/vote")
# def vote():
#     pass
