methods{
    getTokenAtIndex(uint256) returns (address) envfree
    getIdOfToken(address) returns (uint256) envfree
    getReserveCount() returns (uint256) envfree
    addReserve(address, address, address, uint256) envfree
    removeReserve(address) envfree
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

invariant indexLessThanCount(address token)
    getReserveCount() >= 1 && getIdOfToken(token) < getReserveCount() 
        // precondition to a specific method
        {
            preserved removeReserve(address t) {
			    require t == token;
                // is this a same assumption? why?
                require getIdOfToken(token) >= 1;
		    }
        }

// todo: make sure the mappings are correlated
 invariant mappingCorrelation(uint256 index, address token)
    ( index != 0 && token != 0 ) => /* todo */ true /* todo */ 
     {
            preserved
            {
                requireInvariant indexLessThanCount(token);
            }
            
            preserved removeReserve(address t) {
			    require t == token;
		    }
        }

// Each reserve in the list has a unique id - otherwise potential of double counting 
invariant indexInjective(address token1, address token2)
    (token1 != token2 && token1 != 0  && token2 != 0 )  => 
        (getIdOfToken(token1) == 0 || getIdOfToken(token1) != getIdOfToken(token2))
    /*  running the invariant gets a violation where the reserveCount index is not empty so lets prove that and then we can assume that indexLessThanCount holds. However this is also not enough 
    */
    {
    // preconditions to all methods
    preserved
        {
            requireInvariant indexLessThanCount(token1);
            requireInvariant indexLessThanCount(token2);
            // todo - prove this first!
            // requireInvariant mappingCorrelation(getIdOfToken(token1), token1);
            // requireInvariant mappingCorrelation(getIdOfToken(token2), token2); 
        }
    }


