from generate_mimc_hash import *
import random


def mimc_commit(msg, random):
    r = 11
    if random:
        r = random.getrandbits(128) % curve_order
    com = MultiMiMC7(91, [msg, r], 11)
    return r, com 


