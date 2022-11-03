methods {
    set(uint, address)                              envfree
    push(address)                                   envfree
    pop()                                           envfree
    removeReplaceFromEnd(uint)                      envfree
    get(uint)                   returns (address)   envfree
    getWithDefaultValue(uint)   returns (address)   envfree
    getArr()                    returns (address[]) envfree
    getLength()                 returns (uint)      envfree
    frequency(address)          returns (uint)      envfree
}

invariant frequencyLessThenTwo(address a)
    frequency(a) < 2

invariant uniqueArray(uint256 i, uint256 j) 
    i != j => (getWithDefaultValue(i) != getWithDefaultValue(j))
    {
        preserved{
            require true;
        }
    }