/**
 * # ERC20 Parametric Example
 *
 * Another example specification for an ERC20 contract. This one using a parametric rule,
 * which is a rule that encompasses all the methods in the current contract. It is called
 * parametric since one of the rule's parameters is the current contract method.
 * To run enter:
 * 
 * certoraRun ERC20.sol --verify ERC20:Parametric.spec --solc solc8.0 --msg "Parametric rule"
 *
 * The `onlyHolderCanChangeAllowance` fails for one of the methods. Look at the Prover
 * results and understand the counter example - which discovers a weakness in the
 * current contract.
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


/// @title If `approve` changes a holder's allowance, then it was called by the holder
rule onlyHolderCanChangeAllowance(address holder, address spender, method f) {

    // The allowance before the method was called
    mathint allowance_before = allowance(holder, spender);

    env e;
    calldataarg args;  // Arguments for the method f
    f(e, args);                        

    // The allowance after the method was called
    mathint allowance_after = allowance(holder, spender);

    assert allowance_after > allowance_before => e.msg.sender == holder,
        "only the sender can change its own allowance";

    // Assert that if the allowance changed then `approve` or `increaseAllowance` was called.
    assert (
        allowance_after > allowance_before =>
        (
            f.selector == sig:approve(address, uint).selector ||
            f.selector == sig:increaseAllowance(address, uint).selector
        )
    ),
    "only approve and increaseAllowance can increase allowances";
}

