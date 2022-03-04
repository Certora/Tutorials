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

// invariants work
invariant bothListsAreCorrelatedHintInv(uint256 reserveId, address t)
    (t != 0 && reserveId != 0) => (getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t) 
    && (t != 0 && reserveId == 0) => (getIdOfToken(t) == reserveId <=> getTokenAtIndex(reserveId) == t)

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

invariant indexLessThanCount(address token)
    (getReserveCount() > 0 => getIdOfToken(token) < getReserveCount()) &&
    (getReserveCount() == 0 => getIdOfToken(token) == 0)
    {
        preserved removeReserve(address t) {
            require t == token;
        }
    }

// 3rd proof
// Id of assets is injective (i.e. different tokens should have distinct ids).
invariant injectiveAssetIds(uint256 i, uint256 j)
    (getTokenAtIndex(i) != 0 && getTokenAtIndex(j) != 0) => (i != j <=> getTokenAtIndex(i) != getTokenAtIndex(j))
    {
        preserved addReserve(address token, address stableToken, address varToken, uint256 fee) {
            requireInvariant bothListsAreCorrelatedHintInv(i, getTokenAtIndex(i));
            requireInvariant bothListsAreCorrelatedHintInv(j, getTokenAtIndex(j));
        }
    }

// 4th proof
// Independency of tokens in list - removing one token from the list doesn't affect other tokens.
invariant independentTokens(address t, address s)
    (t != 0 && s != 0 && getIdOfToken(t) != 0 && getIdOfToken(s) != 0) => 

rule independentTokens(address t, address s) {
    require(t != 0 && s != 0 && t != s);
    require(getReserveCount() > 2);
    uint256 i = getIdOfToken(t);
    uint256 j = getIdOfToken(s);
    require(i != j);
    removeReserve(t);
    assert(getIdOfToken(s) == j);
}
