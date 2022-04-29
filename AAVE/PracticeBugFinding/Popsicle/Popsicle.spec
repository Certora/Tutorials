/* This spec file shows how to reference ethBalance and take into account calling an external function */

methods {
    currentBalance(address user) returns (uint256) envfree
    ethBalance(address user) returns(uint) envfree
    balanceOf(address user) returns(uint) envfree
    accounts(address user) returns(uint,uint) envfree
    currentUpdate() returns(uint) envfree
    /* The DISPATCHER summary handles each call to the declared method as if any method with the same signature in any target contract may be called */
    acceptEth() => DISPATCHER(true);
}

//total assets of a user is the internal asset (including rewards) and his eth balance
function totalAssetOfUser(address u) returns mathint {
    return currentBalance(u) + ethBalance(u);
}

function getUserLastUpdate(address user) returns uint {
    uint256 latestUpdate;
    uint256 rewards;
    latestUpdate, rewards = accounts(user);
    return latestUpdate; 
}

/*
This rule defines when a user's eth balance can change:
1. It can decrease only if calling deposit  or transferring eth via the OwnerDoItsJobAndEarnsFeesToItsClients method
2. It can increase if collecting fees or withdrawing (we can not require "only if" since it is possible to withdraw 0)
*/
rule validChangeToEthBalance(address u, method f) {
    require u != currentContract; 
    uint256 before = ethBalance(u);
    env e;
    calldataarg args;
    f(e,args);
    uint256 after = ethBalance(u);
    assert before > after <=> 
                ( ( f.selector == deposit().selector || f.selector == OwnerDoItsJobAndEarnsFeesToItsClients().selector ) && 
                e.msg.value > 0 && 
                e.msg.sender == u )   ;
    assert after > before => ( f.selector == withdraw(uint256).selector || f.selector == collectFees().selector );
}

