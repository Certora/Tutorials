
methods {
    currentBalance(address user) returns (uint256) envfree
    ethBalance(address user) returns(uint) envfree
    balanceOf(address user) returns(uint) envfree
    accounts(address user) returns(uint,uint) envfree
    currentUpdate() returns(uint) envfree
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

// a unit-test rule that checks transfer 
rule totalAssetOfUserPreserved(method f, address a, address b, uint256 amount) {
    env e;
    mathint total_balance_before_a_and_b = totalAssetOfUser(a) + totalAssetOfUser(b);
    require e.msg.sender == a;
    transfer(e, b, amount);
    assert ( totalAssetOfUser(a) + totalAssetOfUser(b) == total_balance_before_a_and_b);
}


// a valid-transition rule that checks that if user has balance then he has also a latestUpdates
invariant validState(address user) 
    balanceOf(user) > 0 => getUserLastUpdate(user) > 0
    {
        preserved {
            require currentUpdate() > 0;
        }
    }

// a valid-state invariant: if there is balance, the latest 
// a valid-transition rule that checks that latestUpdate is updated on every change to balance
rule changeToLastUpdated(method f, address user) {
    uint256 balanceBefore = balanceOf(user);
    
    env e;
    calldataarg args;
    f(e,args);

    uint256 latestUpdateAfter = getUserLastUpdate(user);
    uint256 balanceAfter = balanceOf(user);
    assert balanceAfter != balanceBefore =>  latestUpdateAfter == currentUpdate();
}


 