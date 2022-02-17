/**
		Specification file for the Certora Prover 

		
		To simulate the execution of all functions in the main contract, 
		you can define a method argument in the rule and use it in a statement.

		Run:
		 	certoraRun BankFixed.sol:Bank --verify Bank:Parametric.spec --solc solc7.6
		
		It discovers an issue in transfer.
		Run also:
		 	certoraRun Bank.sol --verify Bank:Parametric.spec --solc solc7.6
		See that this rule also uncovers the issue detected by the integrity of deposit rule.
		

**/


rule validityOfTotalFunds(method f) {
	env e; 
	
	require  getTotalFunds(e) >= getFunds(e, e.msg.sender);
	
	// execute some method
   	calldataarg arg; // any argument
	f(e, arg);
	
	assert ( getTotalFunds(e) >= getFunds(e, e.msg.sender), "Total funds are less than user funds" );
}


// Adding local variables can help understanding counter examples
rule validityOfTotalFundsWithVars(method f, uint256 userFundsBefore) {
	env e; 
	address account = e.msg.sender;
	
	require  userFundsBefore == getFunds(e, account);
	uint256 totalBefore = getTotalFunds(e);

	require totalBefore >= userFundsBefore;
	
	// execute some method
   	calldataarg arg; // any argument
	f(e, arg);

	uint256 userFundsAfter = getFunds(e, account);
	uint256 totalAfter = getTotalFunds(e);
	
	assert ( totalAfter >= userFundsAfter, "Total funds are less than user funds" );
}
