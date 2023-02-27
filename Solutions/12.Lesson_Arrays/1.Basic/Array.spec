methods {
	getLength() returns (uint) envfree
    getWithDefaultValue(uint) returns (address) envfree
	isListed(address) returns (bool) envfree
}


invariant inArrayIsListed(uint256 i)
	(i < getLength()) => isListed(getWithDefaultValue(i))


invariant uniqueArraySol(uint256 i, uint256 j)
    i != j => (
        (getWithDefaultValue(i) != getWithDefaultValue(j)) || 
		((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0))
	)
	{
		preserved {
			requireInvariant inArrayIsListed(i);
			requireInvariant inArrayIsListed(j);
		}
	}
