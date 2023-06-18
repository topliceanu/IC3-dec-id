pragma circom 2.0.0;

include "mimc.circom";

template MiMCTest() {
    signal input x;
    signal input k;
    signal input expected;

    component hashing = MiMC7(91);
    hashing.x_in <== x;
    hashing.k <== k;
    log(hashing.out);
    expected === hashing.out;
   
}

component main = MiMCTest();