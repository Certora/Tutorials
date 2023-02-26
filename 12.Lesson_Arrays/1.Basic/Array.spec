// #contract Array.sol:Array
methods {
    get(uint) returns (address) envfree
}


invariant uniqueArrayUsingRevert(uint256 i, uint256 j)
(
    (get@withrevert(i) == get@withrevert(j)) => (i == j)
)


invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((get(i) != get(j)) || ((get(i) == 0) && (get(j) == 0)))
