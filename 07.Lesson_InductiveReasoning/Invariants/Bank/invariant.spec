methods{
    getEthBalance(address) returns uint256 envfree
    getFunds(address) returns uint256 envfree
    getTotalFunds() returns uint256 envfree
}

/**
 * This rule is intended to check that the Bank always returns the user's
 * funds, even if we consider examples where the call to `withdraw` reverts.
 *
 * If `withdraw` does revert, the user's ETH balance will not change, so the
 * rule will fail.
 *
 * This rule does fail because there are lots of uninteresting ways for a
 * function to revert.  For example, a non-payable method will revert if the
 * `msg.value` is nonzero.
 *
 * There are also interesting ways for `withdraw` to revert.  In particular, if
 * the bank gets hacked, it may not _have_ the ETH to return to the user, so
 * the call to `send` would fail.  See `README.md` for a discussion on how to
 * ignore the uninteresting cases and still catch the interesting cases.
 *
 * @dev The `@withrevert` annotation on the call to `withdraw` instructs the
 *      Prover to consider reverting calls, which are ignored by default.
 */
rule can_withdraw_attempt() {
    env e;

    uint256 user_balance_before = getEthBalance(e.msg.sender);
    uint256 user_funds_before   = getFunds(e.msg.sender);

    withdraw@withrevert(e);

    uint256 user_balance_after  = getEthBalance(e.msg.sender);

    assert user_balance_after == user_balance_before + user_funds_before,
        "withdraw must increase sender's ETH balance by `getFunds(sender)`";
}

/**
 * The total funds in the bank is larger than any individual's balance.
 *
 * @dev This doesn't pass for technical reasons, see `README.md` for discussion
 */
invariant totalFunds_GE_single_user_funds_attempt(address user)
    getTotalFunds() >= getFunds(user)

/* A declaration of a ghost.
 * A ghost is, in esssence, an uninterpeted function (remember lesson 3?).
 * This ghost takes no arguments and returns a type mathint.
 */
ghost sum_of_all_funds() returns uint256{
    // for the constructor - assuming that on the constructor the value of the ghost is 0
    init_state axiom sum_of_all_funds() == 0;
}

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
  havoc sum_of_all_funds assuming sum_of_all_funds@new() == sum_of_all_funds@old() + new_balance - old_balance;
}

invariant totalFunds_GE_to_sum_of_all_funds()
    getTotalFunds() >= sum_of_all_funds()
