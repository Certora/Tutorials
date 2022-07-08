// erc20 methods
methods {
    balanceOf(address)                    returns (uint256)
    transfer(address,uint256)             returns (bool)

    allowance(address,address)            returns (uint)
    transferFrom(address,address,uint256) returns (bool)
    approve(address,uint256)              returns (bool)
}

/**** for introduction ****/

/// if you call transfer and you have the funds, your balance decreases and
/// recipient's balance increases
rule transferSpec {
    // TODO
}

// TODO: Run and view a counterexample - didn't specify recipient and sender
//       are different
//
// TODO: fix the counterexample

/**** for last reverted ****/

/// if you call transfer and you don't have the funds, the transaction
/// reverts
rule transferReverts {
    // TODO
}

/**** quick example, not a lot of detail ****/

/// if you call transfer and do have enough funds, the transaction doesn't
/// revert
rule transferDoesntRevert {
    // TODO
}

/**** Exercises ****/

// TODO: as above but for transferFrom

/**** Parametric examples ****/

/// only msg.sender can change their allowance
rule onlyOwnerCanApprove {
    // TODO
}

/// only approve changes allowances
rule onlyApproveChangesAllowances {
    // TODO

    require allowance_before != allowance_after;

    assert f.selector == approve(address, uint).selector;
}

rule withoutApproveAllowanceDoesntChange(method f)
filtered { f -> f.selector != approve(address, uint).selector }
{
    assert allowance_before == allowance_after;
}

/**** "Flex" examples ****/

/// balance changes correspond to borrow changes
/// @dev Armen's example from Nurit
rule totalSupplyCorrelatedWithTotalBalances {
}

/**** Exercises ****/

/// TODO: rules for how balance can change

