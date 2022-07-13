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
    require sender != recip; require other != sender;

    uint balance_sender_before = balanceOf(sender);
    uint balance_recip_before  = balanceOf(recip);

    transfer(e, recip, amount);

    uint balance_sender_after = balanceOf(sender);
    uint balance_recip_after  = balanceOf(recip);

    assert balance_sender_after == balance_sender_before - amount;
    assert balance_recip_after  == balance_recip_before  + amount;
}

