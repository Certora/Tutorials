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
    //optional methods
    increaseAllowance(address spender, uint256 increment)
    decreaseAllowance(address spender, uint256 increment)
}

/*
    Property: Verify that there is no fee on transferFrom() and similarly on transfer (like potentially on USDT)

    This property is implemented as a unit-test style rule - it checks one method but on all possible scenarios.
    Note that it also takes into account all possible values of alice,bob, msg.sender, amount, and of the current state 
    
    Formula (written in Hoare Logic):
        {
            alice != bob 
            balances[bob] = y
            allowance(alice, msg.sender) >= amount
        }

        transferFrom(alice, bob, amount)

        {
            balances[bob] = y + amount
        }


*/
rule noFeeOnTransferFrom(address alice, address bob, uint256 amount) {
    env e; /* a representation of the calling context (msg.sender, block.timestamp, ... ) */
    require alice != bob; /* without this require you will get a counter example in which alice and bob are the same address  */
    // require allowance(alice, e.msg.sender) >= amount;
    uint256 balanceBefore = balanceOf(bob);

    transferFrom(e, alice, bob, amount); 

    uint256 balanceAfter = balanceOf(bob);
    assert balanceAfter == balanceBefore + amount;
}


rule noFeeOnTransfer(address bob, uint256 amount) {
    env e;
    require bob != e.msg.sender;
    uint256 balanceSenderBefore = balanceOf(e.msg.sender);
    uint256 balanceBefore = balanceOf(bob);

    transfer(e, bob, amount);

    uint256 balanceAfter = balanceOf(bob);
    uint256 balanceSenderAfter = balanceOf(e.msg.sender);
    assert balanceAfter == balanceBefore + amount;
}

/*
    Token transfer works correctly. Balances are updated if not reverted. 
    If reverted then the transfer amount was too high, or the recipient is 0.

    Formula:
        {
            balanceFromBefore = balanceOf(from)
            balanceToBefore = balanceOf(to)
        }

        transferFrom(from, to, amount)

        {
            balanceOf(to) = balanceToBefore + amount &&
            balanceOf(from) = balanceFromBefore - amount
        }

    Notes:
        This rule fails on tokens with a blacklist function, like USDC and USDT.
        The prover finds a counterexample of a reverted transfer to a blacklisted address or a transfer in a paused state.



*/


rule transferFromCorrect(address from, address to, uint256 amount, method f) filtered {f -> f.selector == transferFrom(address,address,uint256).selector || f.selector == transferFrom(address,address,uint256).selector } {
    env e;
    // require e.msg.value == 0;
    uint256 fromBalanceBefore = balanceOf(from);
    uint256 toBalanceBefore = balanceOf(to);
    uint256 allowanceBefore = allowance(from, e.msg.sender);
    // require fromBalanceBefore + toBalanceBefore <= max_uint256;

    transferFrom(e, from, to, amount);

    assert from != to =>
        balanceOf(from) == fromBalanceBefore - amount &&
        balanceOf(to) == toBalanceBefore + amount &&
        allowance(from, e.msg.sender) == allowanceBefore - amount;
}

/*
    Property: TransferFrom should revert if and only if the amount is too high or the recipient is 0.

    This rule uses the lastReverted keyword that is set to true on cases that the last method call reverted.

    Formula:
        {
            allowanceBefore = allowance(alice, bob)
            fromBalanceBefore = balanceOf(alice)
        }

        transferFrom(alice, bob, amount)

        {
            lastReverted <=> allowanceBefore < amount || amount > fromBalanceBefore || to = 0
        }

*/
rule transferFromReverts(address from, address to, uint256 amount) {
    env e;
    uint256 allowanceBefore = allowance(from, e.msg.sender);
    uint256 fromBalanceBefore = balanceOf(from);
    uint256 toBalanceBefore = balanceOf(to);
     
    // require from != 0;
    // require e.msg.sender != 0;
    require e.msg.value == 0;
    require fromBalanceBefore + balanceOf(to) <= max_uint256;

    transferFrom@withrevert(e, from, to, amount);

    assert lastReverted <=> (allowanceBefore < amount || amount > fromBalanceBefore || to == 0);
}

rule transferReverts(address from, address to, uint256 amount) {
    env e;
    uint256 fromBalanceBefore = balanceOf(e.msg.sender);
    // require e.msg.sender != 0;
    require e.msg.value == 0;
    require fromBalanceBefore + balanceOf(to) <= max_uint256;

    transfer@withrevert(e, to, amount);

    assert lastReverted <=> ( amount > fromBalanceBefore || to == 0);
}

/*
    Property : Contract calls don't change token total supply.
    This rule is implemented as a parametric rule - it is checked on every method of the contract 
    Formula:
        {
            supplyBefore = totalSupply()
        }

        < call any function >
        
        {
            totalSupply() = supplyBefore
        }

    This rule should fail for any token that has functions that change totalSupply(), like mint() and burn().
    It's still important to run the rule and see if it fails in functions that _aren't_ supposed to modify totalSupply()

    
*/
rule noChangeTotalSupply(method f) {
    // require f.selector != burn(uint256).selector && f.selector != mint(address, uint256).selector;
    uint256 totalSupplyBefore = totalSupply();
    env e;
    calldataarg args;
    f(e, args);
    assert totalSupply() == totalSupplyBefore;
}

/*
    Property: Balance of address 0 is always 0

    Formula:
        { balanceOf[0] = 0 }

    This property is implemented as an invariant. 
    Invariants are a specification of a condition that should always be true once an operation is concluded.
    In addition, the invariant also checks that it holds right after the constructor of the code runs.

*/
invariant ZeroAddressNoBalance()
    balanceOf(0) == 0




/*
    Property : Allowance changes correctly as a result of calls to approve, transfer, increaseAllowance, decreaseAllowance
    This rule shows usage of if statement in CVL.
    If a method does not exist in the code than the rule if skipped  

    Formula:
        {
            allowanceBefore = allowance(from, spender)
        }

        < call any function >

        {
            f.selector = approve(spender, amount) => allowance(from, spender) = amount
            f.selector = transferFrom(from, spender, amount) => allowance(from, spender) = allowanceBefore - amount
            f.selector = decreaseAllowance(spender, delta) => allowance(from, spender) = allowanceBefore - delta
            f.selector = increaseAllowance(spender, delta) => allowance(from, spender) = allowanceBefore + delta
            generic f.selector => allowance(from, spender) == allowanceBefore
        }

    @Notes:
        Some ERC20 tokens have functions like permit() that change allowance via a signature. 
        The rule will fail on such functions.

    @Link:

*/
rule changingAllowanceWithIncreaseDecrease(method f, address from, address spender) 
    {
    // require(decreaseAllowance(address, uint256).selector in currentContract);
    uint256 allowanceBefore = allowance(from, spender);
    env e;
    if (f.selector == approve(address, uint256).selector) {
        address spender_;
        uint256 amount;
        approve(e, spender_, amount);
        if (from == e.msg.sender && spender == spender_) {
            assert allowance(from, spender) == amount;
        } else {
            assert allowance(from, spender) == allowanceBefore;
        }
    } else if (f.selector == transferFrom(address,address,uint256).selector) {
        address from_;
        address to;
        address amount;
        transferFrom(e, from_, to, amount);
        uint256 allowanceAfter = allowance(from, spender);
        if (from == from_ && spender == e.msg.sender) {
            assert from == to || allowanceBefore == max_uint256 || allowanceAfter == allowanceBefore - amount;
        } else {
            assert allowance(from, spender) == allowanceBefore;
        }
       } else if( f.selector == decreaseAllowance(address, uint256).selector) {
        address spender_;
        uint256 amount;
        // require amount <= allowanceBefore;
        decreaseAllowance(e, spender_, amount);
        if (from == e.msg.sender && spender == spender_) {
            assert allowance(from, spender) == allowanceBefore - amount;
        } else {
            assert allowance(from, spender) == allowanceBefore;
        }
    } else if ( f.selector == increaseAllowance(address, uint256).selector) {
        address spender_;
        uint256 amount;
        // require amount + allowanceBefore < max_uint256;
        increaseAllowance(e, spender_, amount);
        if (from == e.msg.sender && spender == spender_) {
            assert allowance(from, spender) == allowanceBefore + amount;
        } else {
            assert allowance(from, spender) == allowanceBefore;
        }
    } else {
        calldataarg args;
        f(e, args);
        assert allowance(from, spender) == allowanceBefore;
    }
}

rule changingAllowanceWithOutIncreaseDecrease(method f, address from, address spender) 
    {
    // require(!decreaseAllowance(address, uint256).selector in currentContract);
    uint256 allowanceBefore = allowance(from, spender);
    env e;
    if (f.selector == approve(address, uint256).selector) {
        address spender_;
        uint256 amount;
        approve(e, spender_, amount);
        if (from == e.msg.sender && spender == spender_) {
            assert allowance(from, spender) == amount;
        } else {
            assert allowance(from, spender) == allowanceBefore;
        }
    } else if (f.selector == transferFrom(address,address,uint256).selector) {
        address from_;
        address to;
        address amount;
        transferFrom(e, from_, to, amount);
        uint256 allowanceAfter = allowance(from, spender);
        if (from == from_ && spender == e.msg.sender) {
            assert from == to || allowanceBefore == max_uint256 || allowanceAfter == allowanceBefore - amount;
        } else {
            assert allowance(from, spender) == allowanceBefore;
        }
    } else {
        calldataarg args;
        f(e, args);
        assert allowance(from, spender) == allowanceBefore;
    }
}

/*
    Property : zero-sum on transfers  
    Transfer from a to b doesn't change the sum of their balances

    Formula
        {
            balancesBefore = balanceOf(msg.sender) + balanceOf(b)
        }

        transfer(b, amount)

        {
            balancesBefore == balanceOf(msg.sender) + balanceOf(b)
        }

    

*/
rule transferSumOfFromAndToBalancesStaySame(address to, uint256 amount) {
    env e;
    mathint sum = balanceOf(e.msg.sender) + balanceOf(to);
    // require sum < max_uint256;
    transfer(e, to, amount); 
    assert balanceOf(e.msg.sender) + balanceOf(to) == sum;
}

rule transferFromSumOfFromAndToBalancesStaySame(address from, address to, uint256 amount) {
    env e;
    mathint sum = balanceOf(from) + balanceOf(to);
    // require sum < max_uint256;
    transferFrom(e, from, to, amount); 
    assert balanceOf(from) + balanceOf(to) == sum;
}

/*
    @Rule

    @Description:
        Transfer from msg.sender to alice doesn't change the balance of other addresses

    @Formula:
        {
            balanceBefore = balanceOf(bob)
        }

        transfer(alice, amount)

        {
            balanceOf(bob) == balanceBefore
        }

    @Notes:

    @Link:

*/
rule transferDoesntChangeOtherBalance(address to, uint256 amount, address other) {
    env e;
    require other != e.msg.sender;
    require other != to;
    uint256 balanceBefore = balanceOf(other);
    transfer(e, to, amount); 
    assert balanceBefore == balanceOf(other);
}

/*
    @Rule

    @Description:
        Transfer from alice to bob using transferFrom doesn't change the balance of other addresses

    @Formula:
        {
            balanceBefore = balanceOf(charlie)
        }

        transferFrom(alice, bob, amount)

        {
            balanceOf(charlie) = balanceBefore
        }

    @Notes:

    @Link:

*/
rule transferFromDoesntChangeOtherBalance(address from, address to, uint256 amount, address other) {
    env e;
    require other != from;
    require other != to;
    uint256 balanceBefore = balanceOf(other);
    transferFrom(e, from, to, amount); 
    assert balanceBefore == balanceOf(other);
}