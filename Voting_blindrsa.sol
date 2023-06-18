// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BlindSigVoting{
    mapping(address => bool) public spent_votes;
    mapping(uint256 => uint256) public options;
    uint256 public endBlock;
    bytes issuer_modulus;
    bytes exp;

    modifier onlyBeforeEnd(){
        require(block.number < endBlock, "Voting has ended");
        _;
    }

    modifier onlyAfterEnd(){
        require(block.number >= endBlock, "Voting has not ended");
        _;
    }
    constructor(uint256 _blockCount, bytes memory issuer_n, bytes memory exponent){
        endBlock = block.number + _blockCount;
        // pk_topic = _pk_topic;
        options[0] = 0;
        options[1] = 0;
        issuer_modulus = issuer_n;
        exp = exponent;
    }

    function memcpy(uint _dest, uint _src, uint _len) pure internal {
        // Copy word-length chunks while possible
        for ( ;_len >= 32; _len -= 32) {
            assembly {
                mstore(_dest, mload(_src))
            }
            _dest += 32;
            _src += 32;
        }

        // Copy remaining bytes
        // Note: this part is commented out as it causes errors
        // Hopefully it's not important!
        /*uint mask = 256 ** (32 - _len) - 1;
        assembly {
            let srcpart := and(mload(_src), not(mask))
            let destpart := and(mload(_dest), mask)
            mstore(_dest, or(destpart, srcpart))
        }*/
    }

    
    function join(
	    bytes memory _s, bytes memory _e, bytes memory _m
    ) pure internal returns (bytes memory) {
        uint inputLen = 0x60+_s.length+_e.length+_m.length;
        
        uint slen = _s.length;
        uint elen = _e.length;
        uint mlen = _m.length;
        uint sptr;
        uint eptr;
        uint mptr;
        uint inputPtr;
        
        bytes memory input = new bytes(inputLen);
        assembly {
            sptr := add(_s,0x20)
            eptr := add(_e,0x20)
            mptr := add(_m,0x20)
            mstore(add(input,0x20),slen)
            mstore(add(input,0x40),elen)
            mstore(add(input,0x60),mlen)
            inputPtr := add(input,0x20)
        }
        memcpy(inputPtr+0x60,sptr,_s.length);
        memcpy(inputPtr+0x60+_s.length,eptr,_e.length);        
        memcpy(inputPtr+0x60+_s.length+_e.length,mptr,_m.length);

        return input;
    }

    function textbookRSAVerify(
        bytes32 _sha256,
        bytes memory _s, bytes memory _e, bytes memory _m
    ) public view returns (bool) {
        

        /// decipher
        bytes memory input = join(_s,_e,_m);
        uint inputlen = input.length;

        uint decipherlen = _m.length;
        uint hashlen = _sha256.length;
        bytes memory decipher = new bytes(decipherlen);
        assembly {
            pop(staticcall(sub(gas(), 2000), 5, add(input,0x20), inputlen, add(decipher,0x20), decipherlen))
        }
        uint i;
        
        for(i=0; i<32; i++){
            //hack to simulate the zero padding difference between len(hash) and len(decryption_output)
            //hope everything else was zeros!
            if (_sha256[i] != decipher[decipherlen - hashlen + i]){
                return false;
            }
        }

        return true;
    }

    function vote(uint256 _option, bytes calldata _sig) public onlyBeforeEnd{
        // Check valid option
        require(_option >= 0 && _option < 2, "Option does not exist");

        // Check vote signature is valid
        address sender_address = msg.sender;
        bytes32 signed_msg = sha256(abi.encodePacked(sender_address));
        require(textbookRSAVerify(signed_msg, _sig, exp, issuer_modulus), "Invalid Signature");
        
        // Check not voted before
        require(!spent_votes[msg.sender], "Already voted");
        spent_votes[msg.sender] = true;

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

    function get_addr(
    ) public view returns (bytes memory) {
        return abi.encodePacked(msg.sender);
    }

    function get_addr_hash(
    ) public view returns (bytes32) {
        return sha256(abi.encodePacked(msg.sender));
    }

}

