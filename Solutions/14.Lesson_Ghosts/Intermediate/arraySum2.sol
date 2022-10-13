// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract arraySum2 {
    uint[] public arr;

    /*
    // Several ways to initialize an array
    uint[] public arr2 = [1, 2, 3];
    // Fixed sized array, all elements initialize to 0
    uint[10] public myFixedSizeArr;
    */
    function get(uint index) public view returns (uint) {
        require(index < arr.length, "index out of bound");

        return arr[index];
    }

    function getWithDefaultValue(uint index) public view returns(uint){
        if (index < arr.length)
        {
            return arr[index];
        }
        return 0;
    }

    function set(uint index, uint value) public {
        require(index < arr.length, "index out of bound");
        arr[index] = value;
    }

    // Solidity can return the entire array.
    // But this function should be avoided for
    // arrays that can grow indefinitely in length.
    function getArr() public view returns (uint[] memory) {
        return arr;
    }

    function push(uint val) public {
        // Append to array
        // This will increase the array length by 1.
        arr.push(val);
    }

    function pushThenChangeValue(uint value) public {
        push(value);
        arr[arr.length - 1] =  value;
    }

    function pop() public {
        // Remove last element from array
        // This will decrease the array length by 1
        arr.pop();

    }

    function getLength() public view returns (uint) {
        return arr.length;
    }

    function removeDelete(uint index) public {
        require(index < arr.length, "index out of bound");

        // Delete does not change the array length.
        // It resets the value at index to it's default value,
        // in this case 0
        delete arr[index];
    }

    // Deleting an element creates a gap in the array.
    // One trick to keep the array compact is to
    // move the last element into the place to delete.
    function removeReplaceFromEnd(uint index) public {
        require(index < arr.length, "index out of bound");
        // Move the last element into the place to delete
        arr[index] = arr[arr.length - 1];
        // Remove the last element
        arr.pop();
    }

    // Remove array element by shifting elements from right to left
    function removeByShifting(uint index) public {
        require(index < arr.length, "index out of bound");
        for (uint i = index; i < arr.length - 1; i++) {
            arr[i] = arr[i + 1];
        }
        arr.pop();
    }

    function swap(uint256 i, uint256 j) public 
    {
        uint256 temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    function getArrSum() public view returns (uint) {
        uint sum = 0;
        for (uint i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }
}