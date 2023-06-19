/**
 * # Fixed ERC20 Example
 *
 * This is the fixed version of ERC20.spec. Note the changes in rule `transferSpec`.
 * Run using:
 *
 * certoraRun ERC20.sol: --verify ERC20:ERC20Fixed.spec --solc solc8.0
 *
 * There should be no errors.
 */

// The methods block below gives various declarations regarding solidity methods.
methods
{
    // When a function is not using the environment (e.g., `msg.sender`), it can be
    // declared as `envfree`
    function balanceOf(address) external returns (uint) envfree;
    function allowance(address,address) external returns(uint) envfree;
    function totalSupply() external returns (uint) envfree;
}


/// @title Transfer must move `amount` tokens from the caller's account to `recipient`
rule transferSpec(address recipient, uint amount) {

    env e;
    
    // `mathint` is a type that represents an integer of any size
    mathint balance_sender_before = balanceOf(e.msg.sender);
    mathint balance_recip_before = balanceOf(recipient);

    transfer(e, recipient, amount);

    mathint balance_sender_after = balanceOf(e.msg.sender);
    mathint balance_recip_after = balanceOf(recipient);

    address sender = e.msg.sender;  // A convenient alias

    // Operations on mathints can never overflow or underflow. 
    assert recipient != sender => balance_sender_after == balance_sender_before - amount,
        "transfer must decrease sender's balance by amount";

    assert recipient != sender => balance_recip_after == balance_recip_before + amount,
        "transfer must increase recipient's balance by amount";
    
    assert recipient == sender => balance_sender_after == balance_sender_before,
        "transfer must not change sender's balancer when transferring to self";
}


/// @title Transfer must revert if the sender's balance is too small
rule transferReverts(address recipient, uint amount) {
    env e;

    require balanceOf(e.msg.sender) < amount;

    transfer@withrevert(e, recipient, amount);

    assert lastReverted,
        "transfer(recipient,amount) must revert if sender's balance is less than `amount`";
}


/** @title Transfer must not revert unless
 * - the sender doesn't have enough funds,
 * - or the message value is nonzero,
 * - or the recipient's balance would overflow,
 * - or the message sender is 0,
 * - or the recipient is 0
 */
rule transferDoesntRevert(address recipient, uint amount) {
    env e;

    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;  // No payment

    // This requirement prevents overflow of recipient's balance.
    // We convert `max_uint` to type `mathint` since:
    //   1. a sum always returns type `mathint`, hence the left hand side is `mathint`,
    //   2. `mathint` can only be compared to another `mathint`
    require balanceOf(recipient) + amount < to_mathint(max_uint);

    // Recall that `address(0)` is a special address that in general should not be used
    require e.msg.sender != 0;
    require recipient != 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}
