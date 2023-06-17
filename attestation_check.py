from nacl.signing import VerifyKey

def is_attestation_valid(attestation) -> bool:
    try:
        pub_key_bytes = bytes.fromhex(attestation['public_key_hex'][2:])
        sig_bytes = bytes.fromhex(attestation['signature_hex'][2:])
        msg_bytes = bytes.fromhex(attestation['data_hex'][2:])

        verify_key = VerifyKey(pub_key_bytes) # public key

        verify_key.verify(msg_bytes, sig_bytes)
        print("Attestation has been verified.")
        return True
    except Exception as err:
        print("Attestation verification has failed.", err)
        return False

