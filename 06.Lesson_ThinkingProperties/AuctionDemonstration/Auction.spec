/* Certora prover verifies calls for all environments. 
   The environment is passed as an additional parameter to functions.
   It can be seen as the following structure, paralleling solidity definitions:
   
    struct env {
         address msg.address // address of the contract being verified
         address msg.sender //  address of the sender of the message 
         uint msg.value  // number of wei sent with the message
         uint block.number // current block number
         uint block.timestamp // current timestamp
         address tx.origin // original transaction sender
    }
    
    An `envfree` method is one that is:
    (1) non-payable (msg.value must be 0)
    (2) does not depend on any environment variable
*/
methods {
    getTotalSupply() returns uint256 envfree
    balanceOf(address) returns uint256 envfree
}

/**************** Generic rules ***********************/
// A rule for verifying that the total supply stays less than MAX_UINT256
rule boundedSupply(method f) {
    // Fetch total supply before
    uint256 _supply = sinvoke getTotalSupply(); 
    
    // Invoke an arbitrary public function on an arbitrary input and take into account only cases that do not revert
    env e; // For every possible environment 
    calldataarg arg;
    sinvoke f(e,arg);
    
    // Fetch total supply after
    uint256 supply_ = sinvoke getTotalSupply(); 
    
    assert _supply != supply_ => 
        supply_ < 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 
        "Cannot increase to MAX_UINT256";   
}

// A rule for verifying that any scenario preformed by some sender does not decrease the balance of any other account.
rule senderCanOnlyIncreaseOthersBalance(method f, address sender, address other)
{  
    // Assume we have two different accounts.
    require other != sender; 
    
    // Get the current balance of the other account
    uint256 origBalanceOfOther = sinvoke balanceOf(other); 

    // Invoke any function with msg.sender being the sender account
    calldataarg arg;
    env ef;
    require ef.msg.sender == sender;
    invoke f(ef, arg);

    uint256 newBalanceOfOther = sinvoke balanceOf(other);

    assert newBalanceOfOther >= origBalanceOfOther, 
        "The balance of the other account decreased"; 
}

// A rule for verifying a correct behavior on sending zero tokens - return false or revert 
rule transferWithIllegalValue(address to)
{
    // Assume the case that `to` is not zero
    require to != 0; 

    env e; // For every possible environment
    // Assume no `msg.value` since this `transferTo` not a payable function
    require e.msg.value == 0; 
    bool res = invoke transferTo(e, to, 0);

    assert lastReverted || !res, 
        "permits a transfer of zero tokens";
}




