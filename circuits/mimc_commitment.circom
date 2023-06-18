pragma circom 2.0.0;

include "mimc.circom";

template MiMCCom() {
    signal input x;
    signal input r;
    signal output com;

    component hashing = MultiMiMC7(2, 91);
    hashing.in <== [x, r];
    hashing.k <== 0;

    com <-- hashing.out;
}

// component main = MiMCCom();