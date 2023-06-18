from generate_mimc_hash import *
import random


def mimc_commit(msg, use_random):
    r = 11
    if use_random:
        r = int(random.getrandbits(128)) % curve_order
    com = MultiMiMC7(91, [msg, r], 0)
    return r, com 


