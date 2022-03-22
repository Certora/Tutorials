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

// sum of 2 accounts' balances cannot be less than a single one of them
invariant twoBalancesGreaterThanSingle(address account1, address account2)
    balanceOf(account1) + balanceOf(account2) < balanceOf(account1) => false

// this rule passes, which means that the above invariant is vacuous since the statement holds for any state and not just as an inductive state
rule checkTaut1(address account1, address account2) {
    uint256 balance1 = balanceOf(account1);
    uint256 balance2 = balanceOf(account2);
    assert ((balance1 + balance2) < balance1) => false;
}
    
// common mistake - not before and after
invariant twoBalancesGreaterThanSingleProb(address account1, address account2)
    balanceOf(account1) + balanceOf(account2) <= balanceOf(account1) + balanceOf(account2) // always equal

// this rule passes, which means that the above invariant is vacuous the statement holds for any state and not just as an inductive state
rule checkTaut2(address account1, address account2) {
    assert balanceOf(account1) + balanceOf(account2) <= balanceOf(account1) + balanceOf(account2);
}

// totalSupply & user's balance ratios
invariant balanceRatios(address account1, address account2)
    totalSupply() == balanceOf(account1) + balanceOf(account2) =>
        (( balanceOf(account1) + balanceOf(account2) == 0 ) =>
            totalSupply() + balanceOf(account1) >= balanceOf(account2) )

// this rule passes, which means that the above invariant is vacuous since the statement holds for any state and not just as an inductive state
rule checkTaut3(address account1, address account2) {
    assert totalSupply() == balanceOf(account1) + balanceOf(account2) =>
        (( balanceOf(account1) + balanceOf(account2) == 0 ) =>
            totalSupply() + balanceOf(account1) >= balanceOf(account2) );
}

rule MethodsVacuityCheck(method f) {
	env e; calldataarg args;
	f(e, args);
	assert false, "this method should have a non reverting path";
}
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
    increaseAllowance(e, spender, amount); // if this reverts, allowance doesnt change and the assert passes
    uint256 allowance_ = allowance(owner, spender);
    assert _allowance <= allowance_;
    assert false, "increaseAllowanceIntegrity has non reverting path";
}

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
    assert false, "transferOutDoesNotChangePowerBalance has non reverting path";
}
// this test passes, which means it is vacuous since there is an assert false at the end

/* Hint: 
 * lastReverted stores information on the last function call only
*/
rule lastRevertedExample(address sender, address recipiecnt, uint256 amount){
    env e;
    uint256 _allownce = allowance(sender, recipiecnt);
    transferFrom@withrevert(e, sender, recipiecnt, amount);
    uint256 allownce_ = allowance(sender, recipiecnt);

    assert lastReverted => _allownce < amount; // last reverted here is the allowance checking function, which doesnt revert, this a vacous check
    assert false, "lastRevertedExample has non reverting path";
}


rule ownerChange(address currentOwner, address user){
    env e; calldataarg args; method f;
    address ownerBefore = _owner(e);
    require currentOwner == ownerBefore && user != currentOwner;
    f(e, args);
    address ownerAfter = _owner(e);
    assert ownerAfter != currentOwner || ownerAfter != user;
    assert false, "ownerChange has non reverting path";
}

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
    assert false, "balanceOfChange has non reverting path";
}

// checks that mint and burn are inverse operations
rule mintBurnInverse(address user, uint256 amount) {
    uint256 balanceBefore = balanceOf(user);
    env e;
    mint(e, user, amount);
    burn(e, user, amount);
    uint256 balanceAfter = balanceOf(user);
    assert balanceBefore == balanceAfter;
    assert false, "mintBurnInverse has non reverting path";
}

