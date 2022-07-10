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

//Run and view a counterexample - didn't specify recipient and sender
//       are different and didn't specify amount is a non-zero amount
// link https://vaas-stg.certora.com/output/93493/1ff00d81d71e881cd6da?anonymousKey=291e8910cc73e67443e9f9c285d4dcc9682e4e53



/// fix the counterexample
/// link https://vaas-stg.certora.com/output/93493/824824706862a17d548a?anonymousKey=08dc8f240c32da2c2624962fc10d4281a09d23af
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

/**** for last reverted ****/

/// if you call transfer and you don't have the funds, the transaction
/// reverts
// link https://vaas-stg.certora.com/output/93493/c8fa900528b5b1aa6537/?anonymousKey=766455cd1cb21286a342a4155ec16b419ba2d99e
rule transferReverts(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) < amount;
    transfer@withrevert(e, recipient, amount);
    assert lastReverted;
}

/**** quick example, not a lot of detail ****/

/// if you call transfer and do have enough funds, the transaction doesn't
/// revert
// payable
// https://vaas-stg.certora.com/output/93493/c50effc27cb05751bba8?anonymousKey=0fb67e37162faa0d78141db49cb961e101396dc0
rule transferDoesntRevert(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// overflow
// https://vaas-stg.certora.com/output/93493/6f01654f7ff1d4d48a54/?anonymousKey=3a6306692c778fddb5d3e32da346a9dd0eb071cd
rule transferDoesntRevert1(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// send to 0
// https://vaas-stg.certora.com/output/93493/b27ededc5b996dfcadea?anonymousKey=1c5156807322eb08b09c043b5c5de0d60307bc19
rule transferDoesntRevert2(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// send from 0
// https://vaas-stg.certora.com/output/93493/bf639a4e5d332e1d7853/?anonymousKey=d15b8038eb4d208d07fd2f7fc0cbb6f4dc4f0c5a
rule transferDoesntRevert3(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require recipient != 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// fixed!
// https://vaas-stg.certora.com/output/93493/cad31dda9c62bb4b21b3/?anonymousKey=e8077ac0a4a4a5971fbf534aa887cb522df1d2db
rule transferDoesntRevert4(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require recipient != 0;
    require e.msg.sender != 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

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

