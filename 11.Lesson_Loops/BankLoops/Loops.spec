methods {
	getTotalFunds() returns (uint256) envfree
    getFunds(address) returns (uint256) envfree
    getEthBalance(address) returns (uint256) envfree
}

/* A declaration of a ghost.
 * A ghost is, in esssence, an uninterpeted function (remember lesson 3?).
 * This ghost takes no arguments and returns a type mathint.
 */
ghost sumAllFunds() returns mathint {
    // for the constructor - assuming that on the constructor the value of the ghost is 0
	init_state axiom sumAllFunds() == 0;
}

/* A hook is a command that is executed upon accessing to storage -
 * on read when Sload is specified, or on write when Sstore is specified.
 * @param funds is the variable for which the hook is tracking its storage
 * @param KEY address user is the key of the mapping funds
 * @param uint256 new_balance is the new value being written to storage
 * @param uint256 old_balance (in the parentheses) is the value that is being replaced upon writing to storage
 */
hook Sstore funds[KEY address user] uint256 new_balance
    // the old value ↓ already there
    (uint256 old_balance) STORAGE {
    /* havoc is a reserved keyword that basically changes the state of the ghost (sumAllFunds) to any state.
     * the assuming command the havoc to take into consideration the following clause.
     * the @new and @old additions to the ghost are incarnations of the ghost
     * we basically say here create new incarnation (@new) that is equal to the old incarnation (@old)
     * plus the difference between the new value stored and the old value stored.
     * remember that the new value is the sum of the old + the an addition, so adding @old to the new will be a wrong count
     */
  havoc sumAllFunds assuming sumAllFunds@new() == sumAllFunds@old() + new_balance - old_balance;
}

// This is an example of an Sload hook
/*
hook Sload uint balance funds[KEY address a] {
	require funds[a] <= getTotalFunds()
}
*/


// This rule fails when a function changes the sum of all funds
rule whoChangedMyGhost(method f) {
	mathint before = sumAllFunds();
	env e;
	calldataarg args;
	f(e,args);
	mathint after = sumAllFunds();
	assert(before == after);
}


// The total funds in the bank is equal to the sum of all individual funds
invariant sumFunds() 
	sumAllFunds() == getTotalFunds()