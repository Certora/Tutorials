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


// Use this hook to update ghosts whenever arrOfTokens is updated
hook Sstore arrOfTokens[INDEX uint256 index] address newValue (address oldValue) STORAGE 
{
	// Here you can update your ghosts whenever arrOfTokens is updated
    require true;
}
// Use this hook to update ghosts whenever arrOfTokens is read
hook Sload address value arrOfTokens[INDEX uint256 index] STORAGE 
{
    require true;
}

// Use the following hooks to update ghosts whenever flag is updated or read
hook Sstore flag[KEY address a] bool newValue (bool oldValue) STORAGE 
{
    require true;
}
hook Sload bool value flag[KEY address a] STORAGE 
{
    require true;
}


invariant flagConsistency(uint256 i)
    (i < getLength()) => getFlag(getWithDefaultValue(i))
    {
        preserved{
            // add here
			require true;
        }
    }

invariant uniqueArray(uint256 i, uint256 j)
    i != j => (
        (getWithDefaultValue(i) != getWithDefaultValue(j)) ||
		((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0))
	)
    {
        preserved{
            // add here
			require true;
        }
    }
