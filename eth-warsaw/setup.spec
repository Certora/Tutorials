/*

    Setup for the EthWarsaw workshop

*/

/*

    Declaration of ERC20 contract methods

*/
methods {
    totalSupply()                         returns (uint256)   envfree
    balanceOf(address)                    returns (uint256)   envfree
    allowance(address,address)            returns (uint256)   envfree
    transfer(address,uint256) returns (bool)
    transferFrom(address,address,uint256) returns (bool)
    approve(address,uint256) returns (bool)
    increaseAllowance(address,uint256) returns (bool)
    decreaseAllowance(address,uint256) returns (bool)
}


/**

    Verify that increaseAllowance is correct.
    This is an example of a unit test rule

*/
rule increaseAllowanceCorrectness() {
    env e;
    address spender;
    uint256 amount;

    uint256 allowanceBefore = allowance(e.msg.sender, spender);
    increaseAllowance(e, spender, amount);
    uint256 allowanceAfter = allowance(e.msg.sender, spender);

    assert allowanceAfter == allowanceBefore + amount;
}

/**

    Only the owner may spend his own balance with the exception of transferFrom function

*/
rule onlyOwnerOrTransferFromChangeBalance(method f)
{
    env e;
    address owner; //
    calldataarg args;
    require owner == e.msg.sender && owner != 0;

    uint256 balanceBefore = balanceOf(owner);
    uint256 allowanceBefore = allowance(owner, e.msg.sender);
    f(e, args);
    uint256 balanceAfter = balanceOf(owner);

    assert balanceAfter < balanceBefore => e.msg.sender == owner || 
        f.selector == transferFrom(address,address,uint256).selector && allowanceBefore >= balanceBefore - balanceAfter;
}

/**

    Exercise 1.
    Write a unit test rule that tests the transfer() function.
    Follow the increaseAllowanceCorrectness example above.

*/

// TODO delete before commit
rule transferCorrectness(address recipient, uint256 amount) {
    env e;

    uint256 balanceSenderBefore = balanceOf(e.msg.sender);
    transfer(e, recipient, amount);
    uint256 balanceSenderAfter = balanceOf(e.msg.sender);

    assert balanceSenderAfter == balanceSenderBefore - amount ;
}

/**

    Exercise 2.
    Write a parametric rule that verifies fixed totalSupply. 
    Follow the onlyOwnerOrTransferFromChangeBalance parametric rule example above

*/
// TODO: delete before commit
rule totalSupplyIsFixed(method f) {
    env e;
    calldataarg args;

    uint256 totalBefore = totalSupply();
    f(e, args);
    uint256 totalAfter = totalSupply();

    assert totalBefore == totalAfter;
}


/**

    Bonus exercise:
        Write a rule that verifies the following property:
            any user can transfer their balance
*/
// TODO: delete in the final version
rule canTransferBalance() {
    env e;
    address recipient;

    require balanceOf(e.msg.sender) > 0;
    require recipient != 0;
    transfer@withrevert(e, recipient, balanceOf(e.msg.sender));
    assert !lastReverted;
    
}