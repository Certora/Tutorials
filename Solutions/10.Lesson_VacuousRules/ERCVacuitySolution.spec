methods{
    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    allowance(address, address) returns (uint256) envfree
    increaseAllowance(address, uint256) returns (bool)
    decreaseAllowance(address, uint256) returns (bool)
    approve(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)
    mint(address, uint256)
    burn(address, uint256)
}    


/**
    TAUTOLOGY -
        LHS of the implication is always false hence the expression is always true.
*/
// sum of 2 accounts' balances cannot be less than a single one of them
invariant twoBalancesGreaterThanSingleFirstTry(address account1, address account2)
    balanceOf(account1) + balanceOf(account2) < balanceOf(account1) => false


/**
    TAUTOLOGY -
        LHS == RHS, regardless of contract's state.
*/
// common mistake - not before and after
invariant twoBalancesGreaterThanSingleSecondTry(address account1, address account2)
    balanceOf(account1) + balanceOf(account2) <= balanceOf(account1) + balanceOf(account2)


/**
    TAUTOLOGY - 
        The only assignment of P,Q,R s.t (P => (Q => R)) == false is
            P = true, Q = true, R = false
        In our case, P = Q = true implies 
            totalSupply == balanceOf1 == balanceOf2 == 0
        hence R can not be false.
*/
// totalSupply & user's balance ratios
invariant balanceRatios(address account1, address account2)
    totalSupply() == balanceOf(account1) + balanceOf(account2) =>
        (( balanceOf(account1) + balanceOf(account2) == 0 ) =>
            totalSupply() + balanceOf(account1) >= balanceOf(account2) )


/**
    NOT VACUOUS -
        To see it, change the behaviour of increaseAllowance.
*/
/* 
 * Try to think about how we can check if this rule is a tautology.
 * It is not as simple as copying the assert to a rule.
 * These problems are being addressed by the Certora team as we try to automate checks for vacuity.
 */
// checks the integrity of increaseAllowance
rule increaseAllowanceIntegrity(address spender, uint256 amount){
    env e;
    address owner;
    require owner == e.msg.sender;
    uint256 _allowance = allowance(owner, spender);
    increaseAllowance(e, spender, amount);
    uint256 allowance_ = allowance(owner, spender);
    assert _allowance <= allowance_;
}

/**
    VACUOUS - Not reachable
        To check it, you can insert a bug to transfer.
*/
// Checks if the correctness of power balance between 2 users is kept.
rule transferOutDoesNotChangePowerBalance(address user1, address user2, address user3, uint256 amount){
    env e; calldataarg args;
    uint256 _balance1; uint256 _balance2;
    require _balance1 == balanceOf(user1);
    require e.msg.sender == user1;
    require _balance2 == balanceOf(user1);
    require _balance1 < _balance2;
    
    transfer(e, user3, amount);

    uint256 balance1_ = balanceOf(user1);
    uint256 balance2_ = balanceOf(user2);

    assert balance1_ < balance2_;
}


/**
    TAUTOLOGY WITH REACHABLE ASSERT - 
        lastReverted refer to allowance instead of transferFrom. 
        Since allowance never reverts, lastReverted == false and the expression in the assert is true.
*/
/* Hint: 
 * lastReverted stores information on the last function call only
*/
rule lastRevertedExample(address sender, address recipiecnt, uint256 amount){
    env e;
    uint256 _allownce = allowance(sender, recipiecnt);
    transferFrom@withrevert(e, sender, recipiecnt, amount);
    uint256 allownce_ = allowance(sender, recipiecnt);

    assert lastReverted => _allownce < amount;
}


/**
    TAUTOLOGY WITH REACHABLE ASSERT - 
        The negation of the assert will be ownerAfter == currentOwner && ownerAfter == user.
        This implies user == currentOwner, contradicting the assumption. 
*/
rule ownerChange(address currentOwner, address user){
    env e; calldataarg args; method f;
    address ownerBefore = _owner(e);
    require currentOwner == ownerBefore && user != currentOwner;
    f(e, args);
    address ownerAfter = _owner(e);
    assert ownerAfter != currentOwner || ownerAfter != user;
}


/**
    TAUTOLOGY WITH REACHABLE ASSERT -
        if balance1Before != balance2Before then user1 != user2
*/
// checks that each function changes balance of at most one user
rule balanceOfChange(method f, address user1, address user2) {
    uint256 balanceOf1Before = balanceOf(user1);
    uint256 balanceOf2Before = balanceOf(user2);
    require !((!(balanceOf1Before < balanceOf2Before)) && (!(balanceOf2Before < balanceOf1Before)));
    env e;
    calldataarg args;
    f(e, args);
    uint256 balanceOf1After = balanceOf(user1);
    uint256 balanceOf2After = balanceOf(user2);
    assert ((balanceOf1After != balanceOf1Before) && 
            (balanceOf2After != balanceOf1Before)) 
               => user1 != user2; 
}


/**
    NOT VACUOUS -
        To check it, you can insert a bug to mint or burn.  
*/
// checks that mint and burn are inverse operations
rule mintBurnInverse(address user, uint256 amount) {
    uint256 balanceBefore = balanceOf(user);
    env e;
    mint(e, user, amount);
    burn(e, user, amount);
    uint256 balanceAfter = balanceOf(user);
    assert balanceBefore == balanceAfter;
}

