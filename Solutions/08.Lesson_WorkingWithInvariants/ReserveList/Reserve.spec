methods{
    getTokenAtIndex(uint256) returns (address) envfree
    getIdOfToken(address) returns (uint256) envfree
    getReserveCount() returns (uint256) envfree
    addReserve(address, address, address, uint256) envfree
    removeReserve(address) envfree
}

// make sure the mappings are correlated
invariant mappingCorrelation(uint256 index, address token)
    (( index != 0 && token != 0 ) => (getTokenAtIndex(index) == token <=> getIdOfToken(token) == index)) 
            &&
	(( index == 0 && token !=0 ) => (getTokenAtIndex(index) == token => getIdOfToken(token) == index))
        {
            preserved
            {
                requireInvariant indexLessThanCount(token);
            }
            
            preserved removeReserve(address t) {
			    require t == token;
		    }
        }

// if the number of elements in the list is non-zero,
// the id of an existing asset must not exceed the number of elements
invariant indexLessThanCount(address token)
    (getReserveCount() > 0 => getIdOfToken(token) < getReserveCount()) &&
    (getReserveCount() == 0 => getIdOfToken(token) == 0)
        {
            preserved removeReserve(address t) {
			    require t == token;
		    }
        }

// each reserve in the list has a unique id
invariant indexInjective(address token1, address token2)
    (token1 != token2) && (token1 != 0 ) && (token2 != 0) => 
        (getIdOfToken(token1) == 0 || (getIdOfToken(token1) != getIdOfToken(token2)))
    {    
        preserved
        {
            requireInvariant indexLessThanCount(token1);
            requireInvariant indexLessThanCount(token2);
            requireInvariant mappingCorrelation(getIdOfToken(token1), token1);
            requireInvariant mappingCorrelation(getIdOfToken(token2), token2);
        }
    }


// removing token from the list doesn't affect other tokens.
// simplifying assumption - other.id != 0
rule removeReserveChangeUnderlyingNonZero(address token, address other) {
    require token != other && token != 0 && other != 0;

    uint256 otherIdBefore = getIdOfToken(other);
    require otherIdBefore != 0;

    requireInvariant indexInjective(token, other);
    requireInvariant mappingCorrelation(otherIdBefore, other);
    
    removeReserve(token);

    uint256 otherIdAfter = getIdOfToken(other);
    uint256 otherById = getTokenAtIndex(otherIdAfter);

    assert other == otherById;
}


// every non-view function changes reserveCount by 1
rule integerityOfCount(method f) {
    env e;
    calldataarg args;
    uint256 reserveCountBefore = getReserveCount();
    f(e, args);
    uint256 reserveCountAfter = getReserveCount();
    assert !f.isView <=> reserveCountBefore - reserveCountAfter == 1 || reserveCountAfter - reserveCountBefore == 1;
}
