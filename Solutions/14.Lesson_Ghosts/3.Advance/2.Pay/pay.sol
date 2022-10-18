pragma solidity ^0.8.0;

import {EnumerableSet} from './EnumerableSet.sol';

contract pay
{
    using EnumerableSet for EnumerableSet.AddressSet;
    EnumerableSet.AddressSet internal _list;  
    //mapping(address => uint256) balances;
    address owner;
    constructor()
    {
        owner = address(0);
    }
    function getLen() public view returns(uint256)
    {
        return _list.values().length;
    }

    function contains(address a) external view returns(bool)
    {
        return _list.contains(a);
    }

    // function getBalance(address a)  external view returns(uint256)
    // {
    //     return balances[a];
    // }

    function getOwner() view public returns(address)
    {
        return owner;
    }
    function add(address user) public
    {
        if (_list.contains(user))
        {
            if (_list.add(user))
            {
                owner = user;
            }
        }
        else{
            _list.add(user);
        }

    }
    function remove() public
    {
        address first = _list.at(0);
        _list.remove(first);
        for (uint256 i = 0; i < getLen(); i++)
        {
            if (_list.at(i) == first )
            {
                owner = first;
            }
        }
    }
}