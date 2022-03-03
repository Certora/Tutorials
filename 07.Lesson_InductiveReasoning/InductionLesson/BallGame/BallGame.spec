
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

	

rule dontGetTo3or4() { // i probably did this wrong?
	// never mind I think this is just the difference between rules and invariants
	env e;
	require ballAt() == 1; // initialize contract?
	pass(e);
	assert ballAt() != 4 && ballAt() != 3;
}

