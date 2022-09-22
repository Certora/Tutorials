pragma solidity ^0.8.6;
contract Offchain {


  function witnessLength(bytes calldata witness) public pure returns (uint256){
    return witness.length;
  }
   function example(bytes32 target, bytes calldata witness) public pure returns (uint256) {
     require(target == keccak256(witness), "BAD_WITNESS");
     return witness.length;
   }

   function exampleViolated(bytes32 target, bytes calldata witness) public pure returns (uint256) {
     require(target == keccak256(witness[:32]), "BAD_WITNESS");
     return witness.length;
   }
}

