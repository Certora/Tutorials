// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Array {
	// NOTE. This solution only prevents *pushing the same address twice*.
	// If an address is popped from the array, it cannot be pushed again.
    address[] public arrOfTokens;

	// A flag indicating if the address is in the list
	mapping (address => bool) public isListed;

	constructor() {
		// Marking 0 as listed, to avoid adding it to the array
		isListed[address(0)] = true;
	}

    function get(uint index) public view returns (address) {
        //Note: reverts when index is out of range 
        return arrOfTokens[index];
    }

    function getWithDefaultValue(uint index) public view returns(address){
        if (index < arrOfTokens.length)
        {
            return arrOfTokens[index];
        }
        return address(0);
    }

    // Solidity can return the entire array.
    // But this function should be avoided for
    // arrays that can grow indefinitely in length.
    function getArr() public view returns (address[] memory) {
        return arrOfTokens;
    }

    function push(address val) public {
        // Append to array
        // This will increase the array length by 1.
		require(!isListed[val]);
        arrOfTokens.push(val);
		isListed[val] = true;
    }

    function pop() public {
        // Remove last element from array
        // This will decrease the array length by 1
        arrOfTokens.pop();
    }

    function getLength() public view returns (uint) {
        return arrOfTokens.length;
    }
}
