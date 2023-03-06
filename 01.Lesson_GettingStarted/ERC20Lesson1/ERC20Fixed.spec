/***
 * # ERC20 Example
 *
 * This is an example specification for a generic ERC20 contract.
 * To run, execute the following command in terminal/cmd:
 *
 *		certoraRun ERC20.sol --verify ERC20:ERC20.spec --solc solc8.0
 *
 *		A simple rule that checks the integrity of the transfer function. 
 *
 *		Understand the counter example and then rerun:
 *
 *		certoraRun ERC20.sol: --verify ERC20:ERC20Fixed.spec --solc solc8.0
 */

methods {
    // When a function is not using the environment (e.g., msg.sender), it can be declared as envfree 
    balanceOf(address)         returns(uint) envfree
    allowance(address,address) returns(uint) envfree
    totalSupply()              returns(uint) envfree
}

//// ## Part 1: Basic rules ////////////////////////////////////////////////////

/// Transfer must move `amount` tokens from the caller's account to `recipient`
rule transferSpec {
    address recip; uint256 amount;

    env e;
    address sender = e.msg.sender;
    // mathint type that represents an integer of any size;
    mathint balance_sender_before = balanceOf(sender);
    mathint balance_recip_before = balanceOf(recip);

    transfer(e, recip, amount);

    mathint balance_sender_after = balanceOf(sender);
    mathint balance_recip_after = balanceOf(recip);

    // operations on mathints can never overflow or underflow. 
    assert recip != sender => balance_sender_after == balance_sender_before - amount,
        "transfer must decrease sender's balance by amount";

    assert recip != sender => balance_recip_after == balance_recip_before + amount,
        "transfer must increase recipient's balance by amount";
    
    assert recip == sender => balance_sender_after == balance_sender_before,
        "transfer must not change sender's balancer when transferring to self";
}


/// Transfer must revert if the sender's balance is too small
rule transferReverts {
    env e; address recip; uint amount;

    require balanceOf(e.msg.sender) < amount;

    transfer@withrevert(e, recip, amount);

    assert lastReverted,
        "transfer(recip,amount) must revert if sender's balance is less than `amount`";
}


/// Transfer must not revert unless
///  the sender doesn't have enough funds,
///  or the message value is nonzero,
///  or the recipient's balance would overflow,
///  or the message sender is 0,
///  or the recipient is 0
///
/// @title Transfer doesn't revert
rule transferDoesntRevert {
    env e; address recipient; uint amount;

    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require e.msg.sender != 0;
    require recipient != 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}
