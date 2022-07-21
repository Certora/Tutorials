
// The sum of 2 vars is GE than 5
invariant xYGE5(uint x, uint y)
    x + y >= 5


// The sum of 2 vars is less than 5
invariant xYL5(uint x, uint y)
    x + y < 5


// The sum of 2 vars is less than 5 or GE 5
invariant Vacuous(uint x, uint y)
    x + y >= 5 || x + y < 5


/****************************************/

// Checks for tautology of the third invariant
rule Vacuous_VacuityCheck(uint x, uint y){
    assert x + y >= 5 || x + y < 5;
}
