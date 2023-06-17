// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingContract{
    mapping(address => bool) public spent_votes;
    mapping(uint256 => uint256) public options;
    uint256 public endBlock;

    modifier onlyBeforeEnd(){
        require(block.number < endBlock, "Voting has ended");
        _;
    }

    modifier onlyAfterEnd(){
        require(block.number >= endBlock, "Voting has not ended");
        _;
    }

    constructor(uint256 _blockCount){
        endBlock = block.number + _blockCount;
        // pk_topic = _pk_topic;
        options[0] = 0;
        options[1] = 0;
    }

    // Input
    // 0, 0xfAce669798EbFA92Ec1e47Adc86b1eA213F564bD, 0x2cd694f8a69312794d7e9444419def719cdd3003ed72d72b6fb44a296e661bcc7617f5442217cb1065d9d0a0e4ac0c411d828b64c093c7a3f4cf627314e066f11b
    function vote(uint256 _option, address _pk_user, bytes calldata _user_sig) public onlyBeforeEnd{
        // Check valid option
        require(_option >= 0 && _option < 2, "Option does not exist");

        // Check vote signature is valid
        bytes32 option_hash = keccak256(abi.encodePacked(_option));
        address recovered_sig = recoverSig(_user_sig, option_hash);
        require(recovered_sig == _pk_user, "Invalid signature");

        // Check not voted before
        require(!spent_votes[_pk_user], "Already voted");
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
        bytes32 r;
        assembly {
            r := calldataload(src)
        }
        src += 0x20;
        bytes32 s;
        assembly {
            s:= calldataload(src)
        }
        return ecrecover(msgHash, v, r, s);
    }
}
