methods {
    get(uint)                   returns (address)   envfree
}

// under assumption 0 is unique
//invariant uniqueArray(uint256 i, uint256 j)
//    i != j => (
 //             (getWithDefaultValue(i) != getWithDefaultValue(j)) || 
 //             (getWithDefaultValue(i) == 0) || 
 //             (getWithDefaultValue(j) == 0)
  //            )



invariant uniqueArray(uint256 i, uint256 j)
(
    (get@withrevert(i) == get@withrevert(j)) => (i == j)
)