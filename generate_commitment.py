from generate_mimc_hash import *
import random


def mimc_commit(msg):
    r = random.getrandbits(128) % curve_order
    print("r = ", r)
    com = MultiMiMC7(91, [msg, r], 11)
    return r, com 

