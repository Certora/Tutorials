rule MethodsVacuityCheck(method f) {
	env e; calldataarg args;
	f(e, args);
	assert false, "this method should have a non reverting path";
}
