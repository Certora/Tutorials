methods {
    getWithDefaultValue(uint) returns (address) envfree
}


/* This invariant will fail on the `push` method of the original Array.sol,
 * as required.
 */
invariant uniqueArraySolution(uint256 i, uint256 j)
    i != j => (
        (getWithDefaultValue(i) != getWithDefaultValue(j)) || 
		((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0))
	)
