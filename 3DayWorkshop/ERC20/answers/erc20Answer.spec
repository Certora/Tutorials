/*
    This is a specification file for the verification of ERC20s
    smart contract using the Certora prover. For more information,
	visit: https://www.certora.com/

*/


////////////////////////////////////////////////////////////////////////////
//                                Methods                                 //
////////////////////////////////////////////////////////////////////////////
/*
    Declaration of methods that are used in the rules. envfree indicate that
    the method is not dependent on the environment (msg.value, msg.sender).
    Methods that are not declared here are assumed to be dependent on env.
*/
methods {
    totalSupply()                         returns (uint256)   envfree
    balanceOf(address)                    returns (uint256)   envfree
    allowance(address,address)            returns (uint)      envfree
}



/*
    Property:No change to 3rd party
    Balance of an address, who is not a sender or a recipient in transfer functions, doesn't decrease 
    as a result of contract calls

    Formula:
        {
            balanceBefore = balanceOf(charlie)
        }

        < call any function >

        {
            f.selector != transfer && f.selector != transferFrom => balanceOf(charlie) == balanceBefore
        }
*/
rule OtherBalanceOnlyGoesUp(address other, method f) {
    env e;
    uint256 balanceBefore = balanceOf(other);

    if (f.selector == transferFrom(address, address, uint256).selector) {
        address from;
        address to;
        uint256 amount;
        require(other != from);
        require balanceOf(from) + balanceBefore < max_uint256;
        transferFrom(e, from, to, amount);
    } else if (f.selector == transfer(address, uint256).selector) {
        require other != e.msg.sender;
        require balanceOf(e.msg.sender) + balanceBefore < max_uint256;
        calldataarg args;
        f(e, args);
    } else {
        require other != e.msg.sender;
        calldataarg args;
        f(e, args);
    }

    assert balanceOf(other) >= balanceBefore;
}

rule transferShouldReturnTrue(address other, method f) {
    env e;
    calldataarg args;
    bool ret = transfer@withrevert(e,args);
    assert !lastReverted => ret;
}