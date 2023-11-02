/* f.selector

 * The use of f.selector is very similar to its use in solidity -
 * since f is a parametric method that calls every function in contract in parallel,
 * we specify (or selecting) to address one particular path - when the f.selector was a specific function.
 */

// Checks that the sum of sender and recipient accounts remains the same after transfer(), i.e. assets doesn't disappear nor created out of thin air
rule integrityOfTransfer(address recipient, uint256 amount) {
	env e;
	uint256 balanceSenderBefore = balanceOf(e, e.msg.sender);
	uint256 balanceRecipientBefore = balanceOf(e, recipient);
	transfer(e, recipient, amount);
	uint256 balanceSenderAfter = balanceOf(e, e.msg.sender);
	uint256 balanceRecipientAfter = balanceOf(e, recipient);

	assert balanceRecipientBefore + balanceSenderBefore == balanceRecipientAfter + balanceSenderAfter, "the total funds before and after a transfer should remain constant";
}


// Checks that transferFrom() correctly decrease allowance of e.msg.sender
rule integrityOfTransferFrom(address owner, address recipient, uint256 amount) {
	env e;
    require owner != recipient; // why is that necessary? try commenting this line out and see what happens
	uint256 allowanceBefore = allowance(e, owner, e.msg.sender);
	transferFrom(e, owner, recipient, amount);
	uint256 allowanceAfter = allowance(e, owner, e.msg.sender);
    
	assert allowanceBefore >= allowanceAfter, "allowance musn't increase after using the allowance to pay on behalf of somebody else";
}


// Checks that increaseAllowance() increases allowance of spender
rule integrityOfIncreaseAllowance(address spender, uint256 amount) {
	env e;
	uint256 allowanceBefore = allowance(e, e.msg.sender, spender);
	increaseAllowance(e, spender, amount);
	uint256 allowanceAfter = allowance(e, e.msg.sender, spender);

	assert amount > 0 => (allowanceAfter > allowanceBefore), "allowance did not increase";
    // Can you think of a way to strengthen this assert to account to all possible amounts?
}


// Users' balance can be changed only as a result of transfer(), transferFrom(), mint(), burn()
rule balanceChangesFromCertainFunctions(method f, address user){
    env e;
    calldataarg args;
    uint256 userBalanceBefore = balanceOf(e, user);
    f(e, args);
    uint256 userBalanceAfter = balanceOf(e, user);

    assert userBalanceBefore != userBalanceAfter => 
        (f.selector == transfer(address, uint256).selector ||
         f.selector == transferFrom(address, address, uint256).selector ||
         f.selector == mint(address, uint256).selector ||
         f.selector == burn(address, uint256).selector),
         "user's balance changed as a result function other than transfer(), transferFrom(), mint() or burn()";
}
