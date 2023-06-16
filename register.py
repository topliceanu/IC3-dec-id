import subprocess
import json

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
    

# with open(DECO_PROVER_CONFIG_FILE, 'r') as file:
#     # output = subprocess.run(command, stdin=file, text=True, capture_output=True)
#     attestation = subprocess.check_output(command, stdin=file, text=True)
#     print(attestation)

if __name__ == "__main__":
    auth_token = "Bearer jufCZwvS3GES9aYbJatwv4GPHzoc7j" # sys.argv[1]
    deco_cfg = get_deco_config(token = auth_token, server_id = "1117987715179348009")
    serialized_cfg = json.dumps(deco_cfg)

    print(serialized_cfg)
    #attestation = subprocess.check_output(command, serialized_cfg, text=True)
    completed = subprocess.run(
        command, 
        input=serialized_cfg,
        text=True,
        capture_output=True,
        # stdout=subprocess.PIPE,
        # Pipes stderr to stdout.
        # stderr=subprocess.STDOUT,
    )
    print(completed.stderr)
    # make commitment
    
    # make zkp

    # ask issuer to verify attestation, commitment, and zkp
