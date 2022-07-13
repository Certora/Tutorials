methods {
    balanceOf(address) returns (uint) envfree
}

/// Transfer must reduce sender's balance by `amount`
/// and increase recipient's balance by `amount`.
/// Transfer must not change any other balance.
rule transferSpec {
    address sender; address recip; uint amount;
    env e;

    require e.msg.sender == sender;
    require sender != recip;

    uint balance_sender_before = balanceOf(sender);
    uint balance_recip_before  = balanceOf(recip);

    transfer(e, recip, amount);

    uint balance_sender_after = balanceOf(sender);
    uint balance_recip_after  = balanceOf(recip);

    assert balance_sender_after == balance_sender_before - amount;
    assert balance_recip_after  == balance_recip_before  + amount;
}

/// Only the owner can decrease their own balance
rule balanceDecreaseOnlyByOwner {
    address owner;

    uint balance_before = balanceOf(owner);

    method f; env e; calldataarg args;
    f(e, args);

    uint balance_after = balanceOf(owner);

    assert balance_after < balance_before => e.msg.sender == owner;
}

/// Zero address always has zero balance
invariant balanceOfZeroIsZero()
    balanceOf(0) == 0

/// Two small transfers gives same balance as one large transfer
rule transferAdditivity {
    address recip; uint amount1; uint amount2; env e;
    address someone;

    storage initialStorage = lastStorage;

    transfer(e, recip, amount1);
    transfer(e, recip, amount2);

    uint balance_after_two_transfers = balanceOf(someone);

    transfer(e, recip, amount1 + amount2) at initialStorage;

    uint balance_after_one_transfer = balanceOf(someone);

    assert balance_after_two_transfers == balance_after_one_transfer;
}


