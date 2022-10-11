

methods {
    set(uint, address)                              envfree
    push(address)                                   envfree
    pop()                                           envfree
    removeDelete(uint)                              envfree
    removeReplaceFromEnd(uint)                      envfree
    removeByShifting(uint)                          envfree
    get(uint)                   returns (address)   envfree
    getWithDefaultValue(uint)   returns (address)   envfree
    getArr()                    returns (address[]) envfree
    getLength()                 returns (uint)      envfree
}


invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((get(i) != get(j)) || ((get(i) == 0) && (get(j) == 0)))