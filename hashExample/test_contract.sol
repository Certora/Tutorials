pragma solidity ^0.8.6;

contract Example {
  function example(bytes32 target, bytes calldata witness) public pure returns (uint256) {
    require(target == keccak256(witness), "BAD_WITNESS");
    return witness.length;
  }
}