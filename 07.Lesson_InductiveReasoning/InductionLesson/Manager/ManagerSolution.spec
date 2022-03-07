methods {
		getCurrentManager(uint256 fundId) returns (address) envfree
		getPendingManager(uint256 fundId) returns (address) envfree
		isActiveManager(address a) returns (bool) envfree
}

rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	env e;
	calldataarg args;
	
	require fundId1 != fundId2;
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);
    require isActiveManager(getCurrentManager(fundId1));			
    require isActiveManager(getCurrentManager(fundId2));
	
	f(e,args);
	
	// verify that the managers are still different 
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
}
		
	
