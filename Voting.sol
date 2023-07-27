// SPDX-License-Identifier: MIT
pragma solidity ^0.8.16;

import {IVerifier} from "IVerifier.sol";

contract VotingContract{
    mapping(address => bool) public spent_votes;
    mapping(uint256 => uint256) public options;
    uint256 public endBlock;
    uint256[2] issuer_pk;

    IVerifier verifier_contract;

    modifier onlyBeforeEnd(){
        require(block.number < endBlock, "Voting has ended");
        _;
    }

    modifier onlyAfterEnd(){
        require(block.number >= endBlock, "Voting has not ended");
        _;
    }

    constructor(uint256 _blockCount, uint256 issuer_x, uint256 issuer_y, address verifier_contract_address){
        endBlock = block.number + _blockCount;
        options[0] = 0;
        options[1] = 0;
        issuer_pk[0] = issuer_x;
        issuer_pk[1] = issuer_y;
        verifier_contract = IVerifier(verifier_contract_address);
    }

    function vote(uint256 _option, address _pk_user, bytes calldata _user_sig, uint[2] calldata _pA, uint[2][2] calldata _pB, uint[2] calldata _pC) public onlyBeforeEnd{
        // Check valid option
        require(_option >= 0 && _option < 2, "Option does not exist");

        // Check vote signature is valid
        bytes32 option_hash = keccak256(abi.encodePacked(_option));
        address recovered_pk = recoverSig(_user_sig, option_hash);
        require(recovered_pk == _pk_user, "Invalid signature");
        uint[] memory pubSignals = new uint[](3);
        pubSignals[0] = issuer_pk[0];
        pubSignals[1] = issuer_pk[1];
        pubSignals[2] = uint256(uint160(recovered_pk));

        // Check not voted before
        require(!spent_votes[_pk_user], "Already voted");

        // Check zk proof of voting qualification
        bool proofIsVerified = verifier_contract.verifyProof(_pA, _pB, _pC, pubSignals);
        require(proofIsVerified, "Invalid proof for the right to vote");

        spent_votes[_pk_user] = true;
        options[_option] = options[_option] + 1;
    }



    function getVoteCount(uint256 _option) public view returns (uint256){
        return options[_option];
    }

    function isDone() public view returns (bool){
        return block.number >= endBlock;
    }

    function getWinningOption() public view returns (uint256){
        uint256 maxVoteCount = 0;
        uint256 winningOption = 0;

        for(uint256 i = 0; i < 2; i++){
            uint256 voteCount = options[i];

            if(voteCount > maxVoteCount){
                maxVoteCount = voteCount;
                winningOption = i;
            }
        }
        return winningOption;
    }

    function recoverSig(bytes calldata sig, bytes32 msgHash) internal pure returns (address) {
        require(sig.length == 65, "Signature length is incorrect");
        uint8 v = uint8(sig[64]);
        uint src;
        assembly {
            src := sig.offset
        }
        bytes32 r2;
        assembly {
            r2 := calldataload(src)
        }
        src += 0x20;
        bytes32 s;
        assembly {
            s:= calldataload(src)
        }
        return ecrecover(msgHash, v, r2, s);
    }
}
