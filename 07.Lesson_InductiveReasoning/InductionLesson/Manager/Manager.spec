methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}



rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	// assume different managers
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);
	
	// hint: add additional variables just to look at the current state
	// bool active1 = isActiveManage(getCurrentManager(fundId1));			
	
	env e;
	calldataarg args;
	f(e,args);
	
	// verify that the managers are still different 
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
}

 /* A start of uniqueManagerAsRule as an invariant, we will see in next lecture how to prove this */


invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
