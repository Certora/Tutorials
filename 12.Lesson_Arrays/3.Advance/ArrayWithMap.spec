methods {
    set(uint, address)                              envfree
    push(address)                                   envfree
    pop()                                           envfree
    removeReplaceFromEnd(uint)                      envfree
    get(uint)                   returns (address)   envfree
    getWithDefaultValue(uint)   returns (address)   envfree
    getArr()                    returns (address[]) envfree
    getLength()                 returns (uint)      envfree
    getFlag(address)            returns (bool)      envfree
}

hook Sstore arrOfTokens[INDEX uint256 index] address newValue (address oldValue) STORAGE 
{
    require true;
}
hook Sload address value arrOfTokens[INDEX uint256 index] STORAGE 
{
    require true;
}


hook Sstore flag[KEY address a] bool newValue (bool oldValue) STORAGE 
{
    require true;
}
hook Sload bool value flag[KEY address a] STORAGE 
{
    require true;
}

invariant flagConsistancy(uint256 i)
    i < getLength() => getFlag(getWithDefaultValue(i))
    {
        preserved{
            // add here
            require true;
        }
    }

invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((getWithDefaultValue(i) != getWithDefaultValue(j)) || ((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0)))
    {
        preserved{
            // add here
            require true;
        }
    }
