/*
This spec was used for the Devcon presentation "bad proofs in formal verification"
*/


// If the user has a token, then the token should exist
rule held_tokens_should_exist {
    address user;
    uint256 token;
    require balanceOf(0, token) == 0;

    // This assumption was proven in a separate rule
    require balanceOf(user, token) <= totalSupplyOf(token);
    assert balanceOf(user, token) > 0 => token_exists(token);
}

// If the user has a token, then the token should exist
rule held_tokens_should_exist {
    address user;
    uint256 token;
    require balanceOf(0, token) == 0;

    assert 0 > 1;
}

// If the rule passes, then it is vacuous
rule held_tokens_should_exist_vacuity_check {
    address user;
    uint256 token;
    require balanceOf(0, token) == 0;

    // This assumption was proven in a separate rule
    require balanceOf(user, token) <= totalSupplyOf(token);
    assert balanceOf(user, token) > 0 => token_exists(token);
    assert false;
}

rule disjoint_precondition {
    uint256 x; uint256 y; uint256 z;
    require x < y;
    require y < z;
    require z < x;
    ...
}

rule something_is_always_transferred {
    address recipient;
    uint256 balance_before_transfer = balanceOf(recipient);
    require balanceOf(recipient) == 0;

    uint256 amount;
    require amount > 0;

    transfer(recipient, amount);

    uint256 balance_after_transfer = balanceOf(recipient);
    assert balanceOf(recipient) <= balance_after_transfer;
}

rule something_is_always_transferred_vacuity_check {
    uint256 balance_after_transfer = balanceOf(recipient);
    assert balanceOf(recipient) <= balance_after_transfer;
}

// WRONG INVARIANT
assert  0 <= i && i < 9 && 
        getBitmapCurrency(account) != 0 &&
        (
            // When a bitmap is enabled it can only have currency masks
            // in the active currencies bytes
            (hasCurrencyMask(account, i) && getActiveUnmasked(account, i) == 0) ||
                getActiveMasked(account, i) == 0
        ) => getActiveUnmasked(account, i) != getBitmapCurrency(account)

rule redundant_precondition {
    address x; address y;
    require balanceOf(x) <= totalSupply();
    
    uint256 sumOfBalances = balanceOf(x) + balanceOf(y);
    require sumOfBalances <= totalSupply();
}

rule tautological_precondition {
    uint256 tot_supply = totalSupply();
    require tot_supply >= 0; 
}

rule sumOfBalancesAfterTransfer {
    address x; address y;
    require x != y;
    uint256 x_balance = balanceOf(a); uint256 y_balance = balanceOf(y);
    amount a;
    transferFrom(x, y, a);

    assert balanceOf(x) + balanceOf(y) == x_balance + y_balance;
}
