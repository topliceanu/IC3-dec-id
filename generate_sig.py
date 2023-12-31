import json
import random
from babyjubjub.ed25519 import *
from generate_commitment import *
from generate_mimc_hash import *
# b = 255
def publickey_l(sk):
    h = str(MiMC7(91, sk, 0))
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    print("public_key_a = ", a)
    A = scalarmult(B, a)
    return A

def Hint_l(m):
    # this is engineered to match the libsnark
    # packing gagdget which willl convert h
    # to a field element
    h = str(MiMC7(91, m, 0))
    tmp = []
    tmp2 = []
    out = 0
    size = 2 * b + 1
    for i in range(size)[::-1]:
        tmp.append(bit(h, i))
        tmp3 = str(bit(h, i)) + "+ " + str(out) + "+ " + str(out) + "=  "
        out = out + out + bit(h, i)

    # reverse endineess and return

    binary = bin(out)[2:][::-1].ljust(size, "0")
    binary = binary[:size]

    return (int(binary, 2))

def generate_keys(use_random):
    sk = 123123
    if use_random:
        sk = int(random.getrandbits(128)) % curve_order

    pk = publickey_l(sk)
    return sk, pk


def mimc_signature(m, sk, pk):
    h = str(MiMC7(91, sk, 0))
    h_int = MiMC7(91, sk, 0)
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    r = Hint_l(int(''.join([h[i] for i in range(int(b // 8), int(b // 4))])) + m) % l
    R = scalarmult(B, 8 * r)
    h = MultiMiMC7(91, [R[0], R[1], pk[0], pk[1], m], 0) % curve_order
    S = (r + (h * a)) % l
    return R, S


def verify_sig(R, S, m, pk):
    A = pk
    h = MultiMiMC7(91, [R[0], R[1], pk[0], pk[1], m], 0)
    if scalarmult(B, 8 * S) != pointAddition(R, scalarmult(A, (8 * h) % l)):
        raise Exception("signature does not pass verification")


def sign_to_json(msg, sk, pk):
    R, S  = mimc_signature(msg, sk, pk)
    data = {
            'enabled': "1",
            'Ax': str(pk[0]),
            'Ay': str(pk[1]),
            'S' : str(S),
            'R8x': str(R[0]),
            'R8y': str(R[1]),
            'M': str(msg)}

    with open('sig_in.json', 'w') as f:
        json.dump(data, f)
    return R, S

def sign_to_data(msg, sk, pk):
    R, S  = mimc_signature(msg, sk, pk)
    data = {
            'enabled': "1",
            'Ax': str(pk[0]),
            'Ay': str(pk[1]),
            'S' : str(S),
            'R8x': str(R[0]),
            'R8y': str(R[1]),
            'M': str(msg)}

    return data, R, S

def sign_to_data_and_com(msg, sk, pk):
    m = msg
    r, msg_com = mimc_commit(m, True)
    R, S = sign_to_json(msg_com, sk, pk)
    data = {
            'voter_PK': str(msg),
            'voter_r': str(r),
            'enabled': "1",
            'Ax': str(pk[0]),
            'Ay': str(pk[1]),
            'S' : str(S),
            'R8x': str(R[0]),
            'R8y': str(R[1]),
            'M': str(msg_com)}

    with open('sig_in.json', 'w') as f:
        json.dump(data, f)
    return R, S


def test_sig():
    sk, pk = generate_keys(True)
    msg = 16204137089086222846243685777293343290570733397750586346311362351531831223551
    sign_to_data_and_com(msg, sk, pk)


#test_sig()

# msg1 = 16204137089086222846243685777293343290570733397750586346311362351531831223551
# _, msg = mimc_commit(msg1, False)
# print(msg)
# R, S = sign_to_json(msg, 123123, pk)
# print("Verified: ", verify_sig(R, S, msg, pk))

# u = MultiMiMC7(91, [11111, 0], 0)
# print("\n Mimc = ", u, "\n")

# u = MiMC7(2, 3, 2)
# print("\n Mimc = ", u, "\n")
