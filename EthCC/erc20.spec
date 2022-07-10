// erc20 methods
methods {
    balanceOf(address)                    returns (uint256) envfree
    transfer(address,uint256)             returns (bool)

    allowance(address,address)            returns (uint)
    transferFrom(address,address,uint256) returns (bool)
    approve(address,uint256)              returns (bool)
}

/**** for introduction ****/

/// if you call transfer and the transaction doesn't revert, your balance decreases and
/// recipient's balance increases
rule transferSpec(env e, address recipient, uint256 amount) {
    uint256 myBalance = balanceOf(e.msg.sender);
    uint256 recipientBalance = balanceOf(recipient);
    transfer(e, recipient, amount);

    //assert myBalance == balanceOf(e.msg.sender) - amount, "sender's balance must decrease by sent amount";
    //assert recipientBalance == balanceOf(recipient) + amount, "recipient's balance must increase by recieved amount";

    // can also do:
    uint256 myBalanceAfter = balanceOf(e.msg.sender);
    uint256 recipientBalanceAfter = balanceOf(recipient);
    assert myBalanceAfter == myBalance - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// // TODO: Run and view a counterexample - didn't specify recipient and sender
// //       are different and didn't specify amount is a non-zero amount

// https://vaas-stg.certora.com/output/93493/1ff00d81d71e881cd6da?anonymousKey=291e8910cc73e67443e9f9c285d4dcc9682e4e53


// // TODO: fix the counterexample
// https://vaas-stg.certora.com/output/93493/824824706862a17d548a?anonymousKey=08dc8f240c32da2c2624962fc10d4281a09d23af
rule transferSpecFixed(env e, address recipient, uint256 amount) {
    require e.msg.sender != recipient;
    uint256 myBalance = balanceOf(e.msg.sender);
    uint256 recipientBalance = balanceOf(recipient);
    transfer(e, recipient, amount);

    //assert myBalance == balanceOf(e.msg.sender) - amount, "sender's balance must decrease by sent amount";
    //assert recipientBalance == balanceOf(recipient) + amount, "recipient's balance must increase by recieved amount";

    // can also do:
    uint256 myBalanceAfter = balanceOf(e.msg.sender);
    uint256 recipientBalanceAfter = balanceOf(recipient);
    assert myBalanceAfter == myBalance - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// /**** for last reverted ****/

// /// if you call transfer and you don't have the funds, the transaction
// /// reverts
// rule transferReverts {
//     // TODO
// }

// /**** quick example, not a lot of detail ****/

// /// if you call transfer and do have enough funds, the transaction doesn't
// /// revert
// rule transferDoesntRevert {
//     // TODO
// }

// /**** Exercises ****/

// // TODO: as above but for transferFrom



// /**** Parametric examples ****/

// /// only msg.sender can change their allowance
// rule onlyOwnerCanApprove {
//     // TODO
// }

// /// only approve changes allowances
// rule onlyApproveChangesAllowances {
//     // TODO

//     require allowance_before != allowance_after;

//     assert f.selector == approve(address, uint).selector;
// }

// rule withoutApproveAllowanceDoesntChange(method f)
// filtered { f -> f.selector != approve(address, uint).selector }
// {
//     assert allowance_before == allowance_after;
// }

// /**** "Flex" examples ****/

// /// balance changes correspond to borrow changes
// /// @dev Armen's example from Nurit
// rule totalSupplyCorrelatedWithTotalBalances {
// }

// /**** Exercises ****/

// /// TODO: rules for how balance can change

