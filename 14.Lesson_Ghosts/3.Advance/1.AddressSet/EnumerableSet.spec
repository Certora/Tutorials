methods {
    contains(address) returns (bool) envfree
    getLen() returns (uint256) envfree
    getVal(uint256) returns (address) envfree
    _removeAddress(address) envfree
    get_mapping_index(address) returns (uint256) envfree
    is_in_set_indexes(address) returns(bool) envfree
    addAddress(address addr) returns (bool) envfree
}

hook Sload bytes32 value _list.(offset 0)[INDEX uint256 index] STORAGE {
    require(to_uint256(value) < max_uint160);
}

invariant uniquenessByIndex(uint256 i, uint256 j)
    (i < getLen() && j < getLen() && i != j) => getVal(i) != getVal(j)
    {
        preserved {
            requireInvariant uniquenessByIndex(i, to_uint256(getLen()-1));
            requireInvariant uniquenessByIndex(j, to_uint256(getLen()-1));
            requireInvariant inverseIndex(i);
            requireInvariant inverseIndex(j);
        }
    }

invariant uniquenessByAddress(address val1, address val2)
        (val1 != val2 && contains(val1) && contains(val2)) => 
        get_mapping_index(val1) != get_mapping_index(val2)
    {
        preserved _removeAddress(address addr) {
            requireInvariant uniquenessByAddress(addr, val1);
            requireInvariant uniquenessByAddress(addr, val2);
            requireInvariant uniquenessByIndex(to_uint256(getLen()-1), to_uint256(get_mapping_index(val1)-1));
            requireInvariant uniquenessByIndex(to_uint256(getLen()-1), to_uint256(get_mapping_index(val2)-1));
        }

        preserved {
            requireInvariant boundedIndex(val1);
            requireInvariant boundedIndex(val2);
            requireInvariant uniquenessByIndex(to_uint256(getLen()-1), to_uint256(get_mapping_index(val1)-1));
            requireInvariant uniquenessByIndex(to_uint256(getLen()-1), to_uint256(get_mapping_index(val2)-1));
        }
    }

invariant containsIntegrityByIndex(uint256 i)
    i < getLen() => contains(getVal(i))
    {
        preserved _removeAddress(address addr){
            requireInvariant inverseIndex(i);
            requireInvariant uniquenessByAddress(addr, getVal(i));
            requireInvariant uniquenessByAddress(addr, getVal(to_uint256(getLen()-1)));
            requireInvariant uniquenessByIndex(i, to_uint256(getLen()-1));
            requireInvariant containsIntegrityByIndex(to_uint256(getLen()-1));
        }
    }

invariant containsIntegrityByAddress(address value)
    0 < get_mapping_index(value) && get_mapping_index(value) < getLen() <=> is_in_set_indexes(value)
    {
        preserved _removeAddress(address addr){
            requireInvariant uniquenessByAddress(addr, value);
            requireInvariant containsIntegrityByAddress(value);
        }
    }

invariant boundedIndex(address value) 
    get_mapping_index(value) <= getLen()
    {
        preserved _removeAddress(address addr){
            requireInvariant boundedIndex(getVal(to_uint256(getLen()-1)));
            requireInvariant inverseValue(value);
            requireInvariant uniquenessByAddress(addr, value);
            requireInvariant uniquenessByAddress(addr, getVal(to_uint256(getLen()-1)));
            requireInvariant uniquenessByAddress(value, getVal(to_uint256(getLen()-1)));
        }

        preserved addAddress(address addr) {
            requireInvariant boundedIndex(getVal(to_uint256(getLen()-1)));
            requireInvariant uniquenessByAddress(addr, value);
            requireInvariant inverseValue(value);
        }
    }

invariant inverseValue(address value)
    contains(value) => getVal(to_uint256(get_mapping_index(value)-1)) == value
    {
        preserved _removeAddress(address addr){
            requireInvariant uniquenessByAddress(addr, value);
            requireInvariant uniquenessByAddress(addr, getVal((to_uint256(getLen()-1))));
            requireInvariant uniquenessByAddress(value, getVal((to_uint256(getLen()-1))));
            //requireInvariant uniquenessByIndex(i, (to_uint256(getLen()-1)));
            //requireInvariant containsIntegrityByIndex(i);
            requireInvariant inverseValue(getVal((to_uint256(getLen()-1))));
        }
    }
    

invariant inverseIndex(uint256 i)
    (i < getLen() && i < max_uint) => (get_mapping_index(getVal(i)) == to_uint256(i+1)) 
    {
        preserved _removeAddress(address addr){
            requireInvariant uniquenessByAddress(addr, getVal((to_uint256(getLen()-1))));
            requireInvariant uniquenessByAddress(addr, getVal(i));
            requireInvariant uniquenessByIndex(i, (to_uint256(getLen()-1)));
        }

        preserved {
            requireInvariant containsIntegrityByIndex(i);
        }
    }

