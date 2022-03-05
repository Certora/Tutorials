
// #1
rule balanceChangeOnTransfers(address recipient, uint256 amount, method f) {
	env e;
    calldataarg args;
	uint256 balanceSenderBefore = balanceOf(e, e.msg.sender);
	uint256 balanceRecipientBefore = balanceOf(e, recipient);
	f(e, args);
    uint256 balanceSenderAfter = balanceOf(e, e.msg.sender);
	uint256 balanceRecipientAfter = balanceOf(e, recipient);

	assert (balanceSenderAfter != balanceSenderBefore &&  balanceRecipientAfter != balanceRecipientBefore) => (f.selector == transfer(address, uint256).selector || f.selector == transferFrom(address, address, uint256).selector)
}

// #2
rule integrityOfTransferFrom(address owner, address recipient, uint256 amount) {
	env e;
    require owner != recipient; // why is that necessary? try commenting this line out and see what happens
	uint256 allowanceBefore = allowance(e, owner, e.msg.sender);
	transferFrom(e, owner, recipient, amount);
	uint256 allowanceAfter = allowance(e, owner, e.msg.sender);
    
	assert allowanceBefore >= allowanceAfter, "allowance musn't increase after using the allowance to pay on behalf of somebody else";
}


// #4
rule supplyChangeNonPublic(address spender, uint256 amount) {
	env e;
    calldataarg args;
    uint256 supplyBefore = totalSupply(e);
    f(e, args);
	uint256 supplyAfter = totalSupply(e);

	assert supplyAfter == supplyBefore, "total supply changed";
}

// #6
rule balanceChangeOnTransfers(address recipient, address other, uint256 amount, method f) {
	env e;
    calldataarg args;
    uint256 balanceOtherBefore = balanceOf(e, other);
	transfer(e, recipient);
    uint256 balanceOtherAfter = balanceOf(e, other);

    assert (balanceOtherBefore == balanceOtherAfter, "trasnfer should not effect others");

}


// # 7 
rule totalSupplyNotLessThanSingleUserBalance(method f, address user) {
	env e;
	calldataarg args;
	uint256 totalSupplyBefore = totalSupply(e);
    uint256 userBalanceBefore = balanceOf(e, user);

    require (f.selector == transfer(address, uint256).selector ||
         f.selector == transferFrom(address, address, uint256).selector ||
         f.selector == burn(address, uint256).selector) => (balanceOf(e, args) + userBalanceBefore) < totalSupplyBefore && (balanceOf(e, e.msg.sender) + userBalanceBefore) < totalSupplyBefore;
    f(e, args);
    
    uint256 totalSupplyAfter = totalSupply(e);
    uint256 userBalanceAfter = balanceOf(e, user);
	assert totalSupplyBefore >= userBalanceBefore => 
            totalSupplyAfter >= userBalanceAfter,
        "a user's balance is exceeding the total supply of token";
}
