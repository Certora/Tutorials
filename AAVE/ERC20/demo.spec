// TODO: write ERC20 specifications

methods {
    // balanceOf doesn't depend on msg.sender, block.timestamp, ...
    balanceOf(address) returns (uint256) envfree;
}


rule transferIncreasesRecipientBalance {
    address recipient;
    address sender;
    uint    amount;

    require sender != recipient;

    mathint balance_before = balanceOf(recipient);

    // call
    env e;
    require e.msg.sender == sender;
    transfer@withrevert(e, recipient, amount);

    mathint balance_after = balanceOf(recipient);

    assert balance_after == balance_before + amount,
        "transfer(recipient,amount) must increase recipient's balance by amount";
}
