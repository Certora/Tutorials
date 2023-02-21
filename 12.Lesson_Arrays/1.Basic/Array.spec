// #contract Array.sol:Array
methods {
    get(uint) returns (address) envfree
}


invariant uniqueArray(uint256 i, uint256 j)
(
    (get@withrevert(i) == get@withrevert(j)) => (i == j)
)
