
methods {
	ballAt() returns uint256 envfree
}

invariant neverReachPlayer4() 
	ballAt() != 4 && ballAt() != 3

	

rule dontGetTo3or4(method f) {
	env e;
	calldataarg args;

	require ballAt() == 1; // initialize contract?
	f(e, args);
	assert ballAt() != 4 && ballAt() != 3;
}

