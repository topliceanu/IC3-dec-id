pragma solidity ^0.8.0;

contract VotingContract{
    // address pk_topic;
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

    function vote(uint256 _option, address _pk_user, bytes calldata _user_sig) public onlyBeforeEnd{
        require(_option >= 0 && _option < 2, "Option does not exist");
        options[_option] = options[_option] + 1;
    }

    function getVoteCount(uint256 _option) public view returns (uint256) {
        return options[_option];
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
