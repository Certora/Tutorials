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



