pragma solidity ^0.8.0;

contract Loops {

// `slow_copy(n)` always returns `n`
    function slow_copy(uint n) public pure returns (uint) {
        uint j = 0;
        for (uint i = 0; i < n; i++)
            j++;
        return j;
    }

// const_loop() always returns 5
    function const_loop() public pure returns (uint) {
        uint j = 0;
        for (uint i = 0; i < 5; i++)
            j++;
        return j;
    }
}