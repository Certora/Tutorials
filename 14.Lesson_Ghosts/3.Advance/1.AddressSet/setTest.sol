// SPDX-License-Identifier: agpl-3.0

pragma solidity ^0.8.0;

import {EnumerableSet} from './EnumerableSet.sol';

contract SetTest {
  using EnumerableSet for EnumerableSet.AddressSet;
  EnumerableSet.AddressSet internal _list;  
  
uint256 constant MAX_UINT256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
  function addAddress(address addr) external returns (bool) 
  {
    return _list.add(addr);  
  }

   function atIndex(uint256 index) external view returns (address) 
  {
    return _list.at(index);  
  }

  function _removeAddress(address addr) external returns(bool) {
    return _list.remove(addr);

  }
  function contains(address a) public view returns(bool)
  {
    return _list.contains(a);
  }

  function getList() external view returns (address[] memory) { 
    return _list.values();
  }

  function getLen() public view returns(uint256)
  {
    return _list.values().length;
  }

  function getVal(uint256 ind) external view returns (address) { 
    if(ind < getLen()) {
      return _list.at(ind);
    }
    else {
      return address(0);
    }
  }

  function get_mapping_index(address addr) external view returns (uint256) {
        uint256 ret;
        if(contains(addr)) {
          ret  = _list.getIndexesVal(addr) + 1 ;  
        }
        else {
          ret = 0; 
        }
        
        return ret;
    }

 // Does address exist in _facilitatorsList.indexes
function is_in_set_indexes(address addr) external view returns(bool)
{
    bool ret = _list.contains(addr);
    return ret;
}


}
