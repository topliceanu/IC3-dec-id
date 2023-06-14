#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import hashlib
import binascii
from ecdsa import SigningKey, VerifyingKey, SECP256k1, util

# Generate private key
sk = SigningKey.generate(curve=SECP256k1)
pk = sk.get_verifying_key()

# Save the public key in a format that's compatible with ecrecover
public_key_bytes = b'\04' + pk.to_string()  # Add the prefix to indicate that it's uncompressed
print("Public Key (hex):", public_key_bytes.hex())

# Create a message
message = b"This is a test message"

# Create a SHA3/Keccak hash of the message
message_hash = hashlib.sha3_256(message).digest()

# Sign the message
signature = sk.sign_digest(message_hash)

# Recover r and s from the signature
r, s = util.sigdecode_string(signature, sk.curve.order)

# Calculate v
v = 27 + ((signature[0] - 27) % 2)

# Display r, s and v in hexadecimal
print("r (hex):", hex(r))
print("s (hex):", hex(s))
print("v (dec):", v)

# Verify the signature
assert pk.verify_digest(signature, message_hash), "Signature verification failed"


# In[ ]:




