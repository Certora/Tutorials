/**
 * # Total Supply Over-Approximation Example
 *
 * The rules here are intended to verify that an ERC20's `totalSupply` method follows
 * the basic property:
 *      For and `address user` we have `totalSupply() >= balanceOf(user)`.
 *
 * First run only the rule `totalSupplyAfterMint`:
 *
 * certoraRun ERC20.sol --verify ERC20:TotalGreaterThanUser.spec --solc --rule totalSupplyAfterMint
 *
 * This rule will fail due to the Prover's tendency to over-approximate the states.
 * Now run the fixed rule `totalSupplyAfterMintWithPrecondition`:
 *
 * certoraRun ERC20.sol --verify ERC20:TotalGreaterThanUser.spec --solc --rule totalSupplyAfterMintWithPrecondition
 *
 * Do you understand why the second rule passed?
 */

// The methods block below gives various declarations regarding solidity methods.
methods
{
    // When a function is not using the environment (e.g., `msg.sender`), it can be
    // declared as `envfree`
    function balanceOf(address) external returns (uint) envfree;
    function allowance(address,address) external returns(uint) envfree;
    function totalSupply() external returns (uint) envfree;
}


/// @title Total supply after mint is at least the balance of the receiving account
rule totalSupplyAfterMint(address account, uint256 amount) {
	env e; 
	
	// Additional variables can aid in understanding violation, like the two below:
	uint256 userBalanceBefore = balanceOf(account);
	uint256 totalBefore = totalSupply();
	
	mint(e, account, amount);
	
	uint256 userBalanceAfter = balanceOf(account);
	uint256 totalAfter = totalSupply();
	
	// Verify that the total supply of the system is at least the current balance of the account.
	assert totalAfter >=  userBalanceAfter, "total supply is less than a user's balance";
}


/** @title Total supply after mint is at least the balance of the receiving account, with
 *  precondition.
 */
rule totalSupplyAfterMintWithPrecondition(address account, uint256 amount) {
	env e; 
	
	uint256 userBalanceBefore = balanceOf(account);
	uint256 totalBefore = totalSupply();
    
    // Assume that in the current state before calling mint, the total supply of the 
    // system is at least the user balance.
    require totalBefore >= userBalanceBefore; 
	
	mint(e, account, amount);
	
	uint256 userBalanceAfter = balanceOf(account);
	uint256 totalAfter = totalSupply();
	
	// Verify that the total supply of the system is at least the current balance of the account.
	assert totalAfter >= userBalanceAfter, "total supply is less than a user's balance ";
}

