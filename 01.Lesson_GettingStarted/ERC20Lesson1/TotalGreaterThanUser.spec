/**
		Specification file for Certora Prover 


		First run only the rule totalSupplyAfterDeposit on the ERC20 contract:
		certoraRun ERC20.sol --verify ERC20:TotalGreaterThanUser.spec --solc solc8.0 --rule totalSupplyAfterMint

		This rule shows that when the initial state the totalSupply was smaller than the user's balance, there is a violation. 

		By adding a precondition we can verify this rule.
		run:

		certoraRun ERC20.sol --verify ERC20:TotalGreaterThanUser.spec --solc solc8.0 --rule totalSupplyAfterMintWithPrecondition

**/

methods {
    // When a function is not using the environment (e.g., msg.sender), it can be declared as envfree 
    balanceOf(address)         returns(uint) envfree
    allowance(address,address) returns(uint) envfree
    totalSupply()              returns(uint) envfree
}

rule totalSupplyAfterMint(address account, uint256 amount) {
	env e; 
	
	// Additional variables to aid in understanding violation:
	
	// uint256 userBalanceBefore = balanceOf(account);
	// uint256 totalBefore = totalSupply();
	
	mint(e, account, amount);
	
	uint256 userBalanceAfter = balanceOf(account);
	uint256 totalAfter = totalSupply();
	
	// Verify that the total supply of the system is at least the current balance of the account.
	assert ( totalAfter >=  userBalanceAfter, "Total supply are less than a user's balance " );
}



rule totalSupplyAfterMintWithPrecondition(address account, uint256 amount) {
	env e; 
	
	uint256 userBalanceBefore = balanceOf(account);
	uint256 totalBefore = totalSupply();
    
    // Assume that in the current state before calling mint, the total supply of the system is at least the user balance.
    require totalBefore >= userBalanceBefore; 
	
	mint(e, account, amount);
	
	uint256 userBalanceAfter = balanceOf(account);
	uint256 totalAfter = totalSupply();
	
	// Verify that the total supply of the system is at least the current balance of the account.
	assert ( totalAfter >=  userBalanceAfter, "Total supply are less than a user's balance " );
}

