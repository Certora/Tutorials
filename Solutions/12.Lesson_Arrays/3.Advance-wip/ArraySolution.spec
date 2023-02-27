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


/* Add a ghost like so:
 * ghost mapping(address => uint256) addressToIndex;
 *
 * Use the hook blocks below to keep you ghosts updated.
 */
// An inverse to get(i)
ghost mapping(address => uint256) addressToIndex;


hook Sstore arrOfTokens[INDEX uint256 index] address newValue (address oldValue) STORAGE 
{
	// Here you can update your ghosts whenever arrOfTokens is updated
	require index < 2 ^ 256 - 1;  // NOTE: this forces index < uint256.max
	require addressToIndex[newValue] == 0;
	require (addressToIndex[oldValue] > 0) => (addressToIndex[oldValue] == index + 1);

	addressToIndex[newValue] = index + 1;
	addressToIndex[oldValue] = 0;

    require true;
}


// addressToIndex is an inverse to get(i)
invariant isInverse(uint256 i)
    i + 1 == addressToIndex[get(i)]


// get(i) == getWithDefaultValue(i) whenever i < getLength()
rule getIsGetWithDefault(uint256 i) {
	address a = get@withrevert(i);
	bool getReverted = lastReverted;
	assert !getReverted => (a == getWithDefaultValue(i)), "Get != GetWithDefault";
	assert getReverted == (i >= getLength()), "Get reverted despite i < getLength()";
}


// addressToIndex is an inverse to getWithDefaultValue(i) (when i < getLength())
invariant isInverseWithDefault(uint256 i)
    (i < getLength()) => (i + 1 == addressToIndex[getWithDefaultValue(i)])
	{
		preserved {
			requireInvariant isInverse(i);  // TODO: check!
		}
	}


invariant flagConsistency(uint256 i)
    (i < getLength()) => getFlag(getWithDefaultValue(i))
    {
        preserved{
			requireInvariant isInverseWithDefault(i);
        }
    }

invariant uniqueArray(uint256 i, uint256 j)
    i != j => (
        (getWithDefaultValue(i) != getWithDefaultValue(j)) ||
		((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0))
	)
    {
        preserved{
			requireInvariant flagConsistency(i);
			requireInvariant flagConsistency(j);
        }
    }
