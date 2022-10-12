// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Array {
    address[] public arrOfTokens;


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

    function set(uint index, address value) public {
        require(index < arrOfTokens.length, "index out of bound");
        arrOfTokens[index] = value;
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
        arrOfTokens.push(val);
    }

    function pop() public {
        // Remove last element from array
        // This will decrease the array length by 1
        arrOfTokens.pop();
    }

    function getLength() public view returns (uint) {
        return arrOfTokens.length;
    }

    // Deleting an element creates a gap in the array.
    // One trick to keep the array compact is to
    // move the last element into the place to delete.
    function removeReplaceFromEnd(uint index) public {
        require(index < arrOfTokens.length, "index out of bound");
        // Move the last element into the place to delete
        arrOfTokens[index] = arrOfTokens[arrOfTokens.length - 1];
        // Remove the last element
        arrOfTokens.pop();
    }
}