methods{
    // getFunds implementation does not require any context to get successfully executed
    getFunds(address) returns (uint256) envfree
    // deposit's implementation uses msg.sender, info that's encapsulated in the environment
    deposit(uint256)

}


rule integrityOfDeposit(uint256 amount) {
	env e; 

	uint256 fundsBefore = getFunds(e.msg.sender);
	deposit(e, amount);	
	uint256 fundsAfter = getFunds(e.msg.sender);

	assert ( fundsBefore + amount == fundsAfter, "Deposit did not increase the funds as expected" );
}

