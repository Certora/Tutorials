methods {
    get(uint)                   returns (address)   envfree
}

invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((get(i) != get(j)) || ((get(i) == 0) && (get(j) == 0)))