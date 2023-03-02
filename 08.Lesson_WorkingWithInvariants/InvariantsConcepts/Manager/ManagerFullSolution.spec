methods {
		getCurrentManager(uint256 fundId) returns (address) envfree
		getPendingManager(uint256 fundId) returns (address) envfree
		isActiveManager(address a) returns (bool) envfree
}

invariant ManagerZeroIsNotActive()
        !isActiveManager(0)


invariant step0_uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2) 
	fundId1 != fundId2 => (getCurrentManager(fundId1) != getCurrentManager(fundId2) )

invariant step1_uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2) 
	fundId1 != fundId2 => (getCurrentManager(fundId1) != getCurrentManager(fundId2) ||
	getCurrentManager(fundId1) == 0 || getCurrentManager(fundId2) == 0  )

invariant step2_activeCurrentManger(uint256 fundId) 
	getCurrentManager(fundId) != 0 => isActiveManager(getCurrentManager(fundId))

invariant step3_activeCurrentManger(uint256 fundId) 
	getCurrentManager(fundId) != 0 => isActiveManager(getCurrentManager(fundId))
	{ 
		preserved claimManagement(uint256 fundIdClaimed) with(env e) {
			require fundIdClaimed == fundId;
		}
	}


invariant step4_uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2) 
	fundId1 != fundId2 => (getCurrentManager(fundId1) != getCurrentManager(fundId2) ||
	getCurrentManager(fundId1) == 0 || getCurrentManager(fundId2) == 0  )
	{ 
		preserved {
			requireInvariant step3_activeCurrentManger(fundId1);
			requireInvariant step3_activeCurrentManger(fundId2);
		}
	}



rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	require fundId1 != fundId2;
    require getCurrentManager(fundId1) != 0 => isActiveManager(getCurrentManager(fundId1));
	require getCurrentManager(fundId2) != 0 => isActiveManager(getCurrentManager(fundId2));
	require getCurrentManager(fundId1) != getCurrentManager(fundId2) ;
				
	env e;
	if (f.selector == claimManagement(uint256).selector)
	{
		uint256 id;
		require id == fundId1 || id == fundId2;
		claimManagement(e, id);  
	}
	else {
		calldataarg args;
		f(e,args);
	}
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
	assert getCurrentManager(fundId1) != 0 => isActiveManager(getCurrentManager(fundId1)), "manager of fund1 is not active";
	assert getCurrentManager(fundId2) != 0 => isActiveManager(getCurrentManager(fundId2)), "manager of fund2 is not active";
}



		
	
