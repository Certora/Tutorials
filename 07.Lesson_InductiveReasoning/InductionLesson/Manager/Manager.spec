methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
	createFund(uint256 fundId);
	claimManagement(uint256 fundId);
}



rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	// assume different managers
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);
	
	require isActiveManager(getCurrentManager(fundId1)) && getCurrentManager(fundId1) != 0;
	require isActiveManager(getCurrentManager(fundId2)) && getCurrentManager(fundId2) != 0;
	requireInvariant managerAssignedInvariant();
	// below doesnt work because like in bug2 contract may not set the activeManager properly
	// require isActiveManager(getCurrentManager(fundId1)) && isActiveManager(getCurrentManager(fundId2));
	// hint: add additional variables just to look at the current state
	// bool active1 = isActiveManageAr(getCurrentManager(fundId1));			
	
	env e;
	calldataarg args;
	f(e,args);
	
	// verify that the managers are still different 
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
}

rule checkManagerAssignment(uint256 fundId, method f) {
	env e;
	calldataarg args;
	require(!isActiveManager(e.msg.sender));
	f(e, args);
	assert(f.selector == claimManagement(uint256).selector || f.selector == createFund(uint256).selector => isActiveManager(e.msg.sender));
}
// need something that states the above rule as an invariant
invariant managerAssignedInvariant(address _manager) {
	// isActiveManager(_manager) => fund[id].manager == _manager 
}

invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2) 
