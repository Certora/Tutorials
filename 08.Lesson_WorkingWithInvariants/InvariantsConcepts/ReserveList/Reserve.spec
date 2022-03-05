methods {
	getTokenAtIndex(uint256) returns (address) envfree
	getIdOfToken(address) returns (uint256) envfree
	getReserveCount() returns (uint256) envfree
	addReserve(address, address, address, uint256) envfree
	removeReserve(address) envfree
}

// first proof
// rules throw
/* rule bothListsAreCorrelatedHintRule(uint256 reserveId, address t) {
    require(t != 0);
    assert(reserveId != 0 => (getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t), "non-zero case: list correlation case failed");
    assert(reserveId == 0 => (getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t), "zero case: list correlation case failed");
} */

/* rule bothListsAreCorrelatedBasic(uint256 reserveId, address t) {
    require(reserveId != 0);
    assert(getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t, "basic case: list correlation failed");
} */

// too loose 
// lets 15 => 401 401 => pass?

// invariants work
invariant bothListsAreCorrelated(uint256 reserveId, address t)
    t != 0 && ((reserveId != 0) => (getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t))
    && ((reserveId == 0) => (getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t))

// basic case throws
// invariant bothListsAreCorrelatedBasicInv(uint256 reserveId, address t) 
//    getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t

// 2nd proof
// There should not be a token saved at an index greater or equal to reserve counter //
invariant reserveCounterIsMaxIndex(uint256 i, address t)
    (i >= getReserveCount()) => getTokenAtIndex(i) == 0 
    // fails when removing tokens, I think spec is right and the code has a bug
    // counter: have 2 tokens ( 0 and 1), reserveCount == 2
    // remove 0, reserve Count == 1
    // token id 1 still exists

// 3rd proof
// Id of assets is injective (i.e. different tokens should have distinct ids).
invariant injectiveAssetIds(uint256 i, uint256 j)
    (getTokenAtIndex(i) != 0 && getTokenAtIndex(j) != 0) => (i != j <=> getTokenAtIndex(i) != getTokenAtIndex(j))
    {
        preserved addReserve(address token, address stableToken, address varToken, uint256 fee) { 
            requireInvariant bothListsAreCorrelated(i, getTokenAtIndex(i));
            requireInvariant bothListsAreCorrelated(j, getTokenAtIndex(j));
        }
    }

// 4th proof
// Independency of tokens in list - removing one token from the list doesn't affect other tokens.
rule independentTokens(address t, address s) {
    require(t != 0 && s != 0 && t != s);
    uint256 i = getIdOfToken(t);
    uint256 j = getIdOfToken(s);
    require(i != j);
    removeReserve(t);
    assert(getIdOfToken(s) == j);
}

// 5th proof
// Each non-view function changes reservesCount by 1.
rule reservesCountChangesByOne(method f) {
    env e;
    calldataarg args;
    require(f.selector == addReserve(address, address, address, uint256).selector || f.selector == removeReserve(address).selector);
    uint256 reserveCountBefore = getReserveCount();
    f(e, args);
    uint256 reserveCountAfter = getReserveCount();
    assert (reserveCountAfter != reserveCountBefore, "no change in reserve count");
    assert (((reserveCountAfter > reserveCountBefore) => (reserveCountAfter - reserveCountBefore == 1)) || ((reserveCountAfter > reserveCountBefore) => (reserveCountAfter - reserveCountBefore == 1)), "change in reserve count not 1");
}