'''
    copyright 2018 to the baby_jubjub_ecc Authors

    This file is part of baby_jubjub_ecc.

    baby_jubjub_ecc is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    baby_jubjub_ecc is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with baby_jubjub_ecc.  If not, see <https://www.gnu.org/licenses/>.
'''

import json

from babyjubjub.ed25519 import *


def toBin(x):
    out = [int(x) for x in bin(int(x, 16))[2:]]
    out = [0] * (256 - len(out)) + out
    return (out)


if __name__ == "__main__":
    sk = "123123"
    m = "4147a3c1586a12cd3ebbc0ad31d6161e10a57894fe2d114d98b509a812918ad0"
    pk = publickey(sk)

    R, S = signature(m, sk, pk)

    # h = Hint(encodepoint(R) + encodepoint(pk) + m)

    checkvalid(R, S, m, pk)

    R[0] = hex(int(''.join(str(e) for e in hexToBinary(hex(R[0]))[::-1]), 2))
    R[1] = hex(int(''.join(str(e) for e in hexToBinary(hex(R[1]))[::-1]), 2))

    pk[0] = hex(int(''.join(str(e) for e in hexToBinary(hex(pk[0]))[::-1]), 2))
    pk[1] = hex(int(''.join(str(e) for e in hexToBinary(hex(pk[1]))[::-1]), 2))

    message = hex(int(''.join(str(e) for e in hexToBinary(m)), 2))
    # print( " h " , h )
    S_bin = toBin(hex(S))

    message_bin = toBin(message)
    pk_x_bin = toBin(pk[0])
    pk_y_bin = toBin(pk[1])

    r_x_bin = toBin(R[0])
    r_y_bin = toBin(R[1])

    # print(S_bin)
    # print (h_bin)

    print("    S.fill_with_bits(pb,  {", S_bin, "});")

    print("    message.fill_with_bits(pb,  {", message_bin, "});")

    print("    pk_x_bin.fill_with_bits(pb,  {", pk_x_bin, "});")
    print("    pk_y_bin.fill_with_bits(pb,  {", pk_y_bin, "});")

    print("    r_x_bin.fill_with_bits(pb,  {", r_x_bin, "});")
    print("    r_y_bin.fill_with_bits(pb,  {", r_y_bin, "});")

    data = {'A': pk_x_bin, 'S' : S_bin, 'Rx': r_x_bin, 'Ry': r_y_bin}

    with open('babyjubjub.cfg', 'w') as f:
        json.dump(data, f)

