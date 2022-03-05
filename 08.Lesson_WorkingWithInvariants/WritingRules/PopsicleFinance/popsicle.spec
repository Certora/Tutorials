methods {	
    // popsicle functions
	deposit() 
	withdraw(uint256) 
    collectFees() 
	OwnerDoItsJobAndEarnsFeesToItsClients() 

    // erc20 functions
    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    transferFrom(address,address, uint256) returns (bool)
    allowanceOf(address , address )  returns (uint256) envfree
    approve(address , uint256 )  returns (bool) 
    increase_allowance(address , uint ) 
    decrease_allowance(address , uint ) 

    // utility functions
    totalAssetsOf(address) returns (uint256) envfree
    getTotalFeesEarnedPerShare() returns (uint256) envfree
    feesCollectedPerShareOf(address) returns (uint256) envfree
    rewardsOf(address) returns (uint256) envfree
    assetsOf(address) returns (uint256) envfree
}

rule popsicleDoesntGetExploited(method f) {
    env e;
    calldataarg args;

    uint256 attackerAssetsBefore = totalAssetsOf(e.msg.sender);
    f(e, args);
    uint256 attackerAssetsAfter = totalAssetsOf(e.msg.sender);

    assert attackerAssetsAfter == attackerAssetsBefore, "attacker gained assets";
}

rule rewardsResetOnCollect(address acct, method f) {
    env e;
    calldataarg args;

    require rewardsOf(e.msg.sender) > 0;
    uint256 rewardsBefore = rewardsOf(e.msg.sender);
    f(e, args);
    uint256 rewardsAfter = rewardsOf(e.msg.sender);

    assert (rewardsAfter<rewardsBefore => f.selector==collectFees().selector, "rewards decreased without being collected");
    assert f.selector==collectFees().selector => rewardsAfter == 0, "all rewards werent collected";
}

rule assetsIncreaseAfterDeposit() {
    env e;

    uint256 assetsBefore = assetsOf(e.msg.sender);
    deposit(e);
    uint256 assetsAfter = assetsOf(e.msg.sender);

    assert assetsAfter >= assetsBefore, "assets decreased after deposit";
}

rule assetsDecreaseAfterWithdraw() {
    env e;

    uint256 assetsBefore = assetsOf(e.msg.sender);
    withdraw(e, balanceOf(e.msg.sender));
    uint256 assetsAfter = assetsOf(e.msg.sender);

    assert assetsAfter <= assetsBefore, "assets increased after withdraw";
}