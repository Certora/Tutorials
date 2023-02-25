/***
 * # ERC20 Example
 *
 * This is an example specification for a generic ERC20 contract.
 * 
 * To simulate the execution of all functions in the main contract, 
 *		you can define a method argument in the rule and use it in a statement.
 *		Run:
 *		 	certoraRun ERC20.sol --verify ERC20:Parametric.spec --solc solc8.0 --msg "parametric rule"
 * 
 */

methods {
    // When a function is not using the environment (e.g., msg.sender), it can be declared as envfree 
    balanceOf(address)         returns(uint) envfree
    allowance(address,address) returns(uint) envfree
    totalSupply()              returns(uint) envfree
}


//// ## Part 2: parametric rules ///////////////////////////////////////////////

/// If `approve` changes a holder's allowance, then it was called by the holder
rule onlyHolderCanChangeAllowance {
    address holder; address spender;

    mathint allowance_before = allowance(holder, spender);

    method f; env e; calldataarg args; 
    f(e, args);                        

    mathint allowance_after = allowance(holder, spender);

    assert allowance_after > allowance_before => e.msg.sender == holder,
        "approve must only change the sender's allowance";

    assert allowance_after > allowance_before =>
        (f.selector == approve(address,uint).selector || f.selector == increaseAllowance(address,uint).selector),
        "only approve and increaseAllowance can increase allowances";
}

