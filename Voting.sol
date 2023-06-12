pragma solidity ^0.8.0;

contract VotingContract{
    struct Option{
        string name;
        uint256 voteCount;
    }

    mapping(string => Option) public options;
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
    }

    function vote(string memory _option) public onlyBeforeEnd{
        Option storage chosenOption = options[_option];
        require(bytes(chosenOption.name).length > 0, "Option does not exist");
        chosenOption.voteCount ++;
    }

    function getVoteCount(string memory _option) public view returns (uint256) {
        return options[_option].voteCount;
    }

    function getWinningOption() public view onlyAfterEnd returns (string memory){
        uint256 maxVoteCount = 0;
        string memory winningOption;

        for(uint256 i = 0; i < 2; i++){
            string memory optionName = ["OptionA", "OptionB"][i];
            uint256 voteCount = options[optionName].voteCount;

            if(voteCount > maxVoteCount){
                maxVoteCount = voteCount;
                winningOption = optionName;
            }
        }
        return winningOption;
    }
}
