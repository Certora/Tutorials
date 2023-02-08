methods{
    x()envfree
    y()envfree
    root() returns address envfree
    a() returns uint envfree
}

// reachability
rule vacuous {
  uint x;
  uint y;
  require x > 2;
  require x < 1;
  assert y == 2, "f must return 2";
}

// Not a tautology
invariant rootNonZero()
    root() != 0


rule rootNonZeroRule(){
    assert root() != 0;
}


// Tautology
invariant aGE0()
    a() >= 0

rule aGE0Rule{
    assert a() >= 0;
}

// Rule implication check p => q
// assert !p
rule sanityImplicationAssertion1{
    uint a;
    uint b;
    assert a<0 => (b<10);
}

// assert q
rule sanityImplicationAssertion2{
    uint a;
    uint b;
    assert a>10 => b>=0;
}

// Double implication p <=> q
// assert(!p && !q)
rule sanityDoubleImplication1{
    uint a;
    uint b;
    assert a<0 <=> b<0;
}

// assert(p && q)
rule sanityDoubleImplication2{
    uint a;
    uint b;
    assert a>=0 <=> b>=0;
}

// Disjunction p || q
// assert p
rule sanityDisjunction1{
    uint a;
    uint b;
    assert a>=0 || b>10;
}
// assert p
rule sanityDisjunction2{
    uint a;
    uint b;
    assert a>10 || b>=0;
}

