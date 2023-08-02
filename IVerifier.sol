// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.16;

interface IVerifier {
    function verifyProof(
        uint256[2] calldata a,
        uint256[2][2] calldata b,
        uint256[2] calldata c,
        uint256[3] calldata input
    ) external view returns (bool);
}
