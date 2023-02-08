// SPDX-License-Identifier: GPL-3.0-or-later
// TODO license

pragma solidity ^0.8.0;
contract sanityCheck{
    uint public x;
    uint public y;

    address public root;
    uint public a;
    constructor(address _root){
        require(_root != address(0));
        root = _root;
    }
    function changeRoot (address root_) public{
        require(root_ != address(0));
        root = root_;
    }
}