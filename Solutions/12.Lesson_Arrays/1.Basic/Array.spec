methods {
    get(uint)                   returns (address)   envfree
    getWithDefaultValue(uint)   returns (address)   envfree
}

invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((get(i) != get(j)) || ((get(i) == 0) && (get(j) == 0)))


invariant uniqueArraySol(uint256 i, uint256 j)
    i != j => ((getWithDefaultValue(i) != getWithDefaultValue(j)) || ((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0)))