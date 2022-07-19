methods{
    slow_copy(uint) returns uint envfree
    const_loop() returns uint envfree
}

// slow_copy() always returns the input value 
rule slow_copy_correct(uint n) {
    assert slow_copy(n) == n, "slow_copy(n) always returns n";
}

// This rule should fail as slow_copy(n) should always return n
rule slow_copy_wrong(uint n) {
    assert slow_copy(n) == 2*n, "slow_copy(n) returned a value other than 2*n";
}

// const_loop always returns 5
rule const_loop_correct(){
    assert const_loop() == 5, "The function returned a value other than 5";
}

// This rule should fail as const_loop should always return 5
rule const_loop_wrong(){
    assert const_loop() == 3, "The function returned a value other than 3";
}