methods {
		getCurrentManager(uint256 fundId) returns (address) envfree
		getPendingManager(uint256 fundId) returns (address) envfree
		isActiveManager(address a) returns (bool) envfree
}



rule uniqueManager(uint256 fundId1, uint256 fundId2, method f) {
	require fundId1 != fundId2;
	require getCurrentManager(fundId1) != 0 && isActiveManager(getCurrentManager(fundId1));
	require getCurrentManager(fundId2) != 0 && isActiveManager(getCurrentManager(fundId2));
	require getCurrentManager(fundId1) != getCurrentManager(fundId2) ;
				
	env e;
	if (f.selector == claimManagement(uint256).selector)
	{
		uint256 id;
		require id == fundId1 || id == fundId2;
		claimManagement(e, id);  
	}
    // correct post condition
    else if (f.selector == createFund(uint256).selector && false) {
        uint256 id;
		// require id != fundId1 && id != fundId2; dont need pre/ bad pre?
        // id == fund1 => createFund(fund1) reverts because of require(funds[fundId].currentManager == address(0)), so doesnt throw;
        // can either add post condition, or remove a pre. This means rule is too soft
		createFund(e, id); 
        assert getCurrentManager(id) != getCurrentManager(fundId1), "managers not different";
        assert getCurrentManager(id) != getCurrentManager(fundId2), "managers not different";
    }
    // only correct pre condition; doesnt work
    else if (f.selector == createFund(uint256).selector) {
        uint256 id;
		require id != fundId1 && id != fundId2;
		createFund(e, id); 
    }
    // only correct post condition; works
    else if (f.selector == createFund(uint256).selector) {
        uint256 id;
		createFund(e, id); 
        assert getCurrentManager(id) != getCurrentManager(fundId1), "managers not different";
        assert getCurrentManager(id) != getCurrentManager(fundId2), "managers not different";
    }
	else {
		calldataarg args;
		f(e,args);
	}
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
	assert getCurrentManager(fundId1) != 0 && isActiveManager(getCurrentManager(fundId1)), "manager of fund1 is not active";
	assert getCurrentManager(fundId2) != 0 && isActiveManager(getCurrentManager(fundId2)), "manager of fund2 is not active";
}


/* A version of uniqueManagerAsRule as an invariant 
invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
	((fundId1 != fundId2) && 
	(getCurrentManager(fundId1) != 0 || getCurrentManager(fundId2) != 0)) => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
    */


		
	
