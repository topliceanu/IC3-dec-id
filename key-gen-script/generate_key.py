#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from ecdsa import SigningKey, SECP256k1

# Generate private key
sk = SigningKey.generate(curve=SECP256k1)
pk = sk.get_verifying_key()

# Save the public key in a format that's compatible with ecrecover
public_key_bytes = b'\04' + pk.to_string()  # Add the prefix to indicate that it's uncompressed

# Save keys to files
with open('private_key.pem', 'w') as f:
    f.write(sk.to_pem().decode())

with open('public_key.pem', 'w') as f:
    f.write(pk.to_pem().decode())

print("Keys generated and saved to files.")

