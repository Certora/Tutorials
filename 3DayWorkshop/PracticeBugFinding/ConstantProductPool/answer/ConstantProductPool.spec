
/***
This example explains many features of Certora Verification Language. 
See https://docs.certora.com for a complete guide.
***/

// reference from the spec to additional contracts used in the verification 
using DummyERC20A as _token0 
using DummyERC20B as _token1


/*
    Declaration of methods that are used in the rules. envfree indicate that
    the method is not dependent on the environment (msg.value, msg.sender).
    Methods that are not declared here are assumed to be dependent on env.
*/

methods{
    token0() returns (address) envfree;
    token1() returns (address) envfree;
    allowance(address,address) returns (uint256) envfree;
    totalSupply()returns uint256 envfree;
    getReserve0() returns uint256 envfree;
    getReserve1() returns uint256 envfree;
    swap(address tokenIn, address recipient) returns (uint256 amountOut) envfree;
    
    //calls to external contracts  
    _token0.balanceOf(address user) returns (uint256) envfree;
    _token1.balanceOf(address user) returns (uint256) envfree;
    _token0.transfer(address, uint);
    _token1.transfer(address, uint);
    transferFrom(address sender, address recipient, uint256 amount) => DISPATCHER(true);
    balanceOf(address) returns (uint256) envfree => DISPATCHER(true);
    
}

// a function for precondition assumptions 
function setup(env e){
    address zero_address = 0;
    uint256 MINIMUM_LIQUIDITY = 1000;
    require totalSupply() == 0 || balanceOf(zero_address) == MINIMUM_LIQUIDITY;
    require balanceOf(zero_address) + balanceOf(e.msg.sender) <= totalSupply();
    require _token0 == token0();
    require _token1 == token1();
}


/*
Property: For all possible scenarios of swapping token1 for token0, the balance of the recipient is updated as expected. 

This property is implemented as a unit-test style rule - it checks one method but on all possible scenarios.
Note that it also takes into account if the recipient is the contract itself, in which case this property does not hold since the balance is unchanged.
As a result, we add a require that the recipient is not the currentContract.

This property catches a bug in which there is a switch between the token and the recipient:
        transfer( recipient, tokenOut, amountOut);

Formula:
        { b = _token0.balanceOf(recipient) }
            amountOut := swap(_token1, recipient);
        { _token0.balanceOf(recipient) = b + amountOut }
*/

rule integrityOfSwap(address recipient) {
    env e;
    setup(e);
    require recipient != currentContract;
    uint256 balanceBefore = _token0.balanceOf(recipient);
    uint256 amountOut = swap(_token1, recipient);
    uint256 balanceAfter = _token0.balanceOf(recipient);
    assert balanceAfter == balanceBefore + amountOut; 
}

/*
Property: Only the user itself or an allowed spender can decrease the user's LP balance.

This property is implemented as a parametric rule - it checks all public/external methods of the contract.

This property catches a bug in which there is a switch between the token and the recipient in burnSingle:
        transfer( recipient, tokenOut, amountOut);

Formula:
        { b = balanceOf(account), allowance = allowance(account, e.msg.sender) }
            op by e.msg.sender;
        { balanceOf(account) < b =>  (e.msg.sender == account  ||  allowance >= (before-balanceOf(account)) }
*/

rule noDecreaseByOther(method f, address account) {
    env e;
    setup(e);
    require e.msg.sender != account;
    require account != currentContract; 
    uint256 allowance = allowance(account, e.msg.sender); 
    
    uint256 before = balanceOf(account);
    calldataarg args;
    f(e,args);
    uint256 after = balanceOf(account);
    
    assert after < before =>  (e.msg.sender == account  ||  allowance >= (before-after))  ;
}


/*
Property: For both token0 and token1 the balance of the system is at least as much as the reserves.

This property is implemented as an invariant. 
Invariants are a specification of a condition that should always be true once an operation is concluded.
In addition, the invariant also checks that it holds right after the constructor of the code runs.

This invariant also catches the bug in which there is a switch between the token and the recipient in burnSingle:
        transfer( recipient, tokenOut, amountOut);

Formula:
    getReserve0() <= _token0.balanceOf(currentContract) &&
    getReserve1() <= _token1.balanceOf(currentContract)
*/

invariant balanceGreaterThanReserve()
    (getReserve0() <= _token0.balanceOf(currentContract))&&
    (getReserve1() <= _token1.balanceOf(currentContract))
    {
        preserved with (env e){
         setup(e);
        }
    }


/*
Property: Integrity of totalSupply with respect to the amount of reserves. 

This is a high level property of the system - the ability to pay back liquidity providers.
If there are any LP tokens (the totalSupply is greater than 0), then neither reserves0 nor reserves1 should ever become zero (otherwise the pool could not produce the underlying tokens).

This invariant catches the original bug in Trident where the amount to receive is computed as a function of the balances and not the reserves.

Formula:
    (totalSupply() == 0 <=> getReserve0() == 0) &&
    (totalSupply() == 0 <=> getReserve1() == 0)
*/

invariant integrityOfTotalSupply()
    
    (totalSupply() == 0 <=> getReserve0() == 0) &&
    (totalSupply() == 0 <=> getReserve1() == 0)
    {
        preserved with (env e){
            requireInvariant balanceGreaterThanReserve();
            setup(e);
        }
    }


/*
Property: Monotonicity of mint.

The more tokens a user transfers to the system the more LP tokens that user should receive. 
This property is implemented as a relational property - it compares two different executions on the same state.

This invariant catches a bug in mint where the LP tokens of the first depositor are not computed correctly and the less he transfers the more LP-tokens he receives. 

Formula:
    { x > y }
        _token0.transfer(currentContract, x); mint(recipient);
        ~ 
        _token0.transfer(currentContract, y); mint(recipient);
    { balanceOf(recipient) at 1  >=  balanceOf(recipient) at 2  }
*/

rule monotonicityOfMint(uint256 x, uint256 y, address recipient) {
    env eT0;
    env eM;
    setup(eM);
    requireInvariant integrityOfTotalSupply();
    storage init = lastStorage;
    require recipient != currentContract;
    require x > y ;
    _token0.transfer(eT0, currentContract, x);
    uint256 amountOut0 = mint(eM,recipient);
    uint256 balanceAfter1 = balanceOf(recipient);
    
    _token0.transfer(eT0, currentContract, y) at init;
    uint256 amountOut2 = mint(eM,recipient);
    uint256 balanceAfter2 = balanceOf(recipient); 
    assert balanceAfter1 >= balanceAfter2; 
}

/*
Property: Sum of balances

The sum of all balances equals the total supply 

This property is implemented with a ghost, an additional variable that tracks changes to the balance mapping

Formula:
    
    sum(balanceOf(u) for all address u) = totalSupply()

*/

ghost mathint sumBalances{
    // assuming value zero at the initial state before constructor 
	init_state axiom sumBalances == 0; 
}


/* here we state when and how the ghost is updated */
hook Sstore _balances[KEY address a] uint256 new_balance
// the old value that balances[a] holds before the store
    (uint256 old_balance) STORAGE {
  sumBalances = sumBalances + new_balance - old_balance;
}

invariant sumFunds() 
	sumBalances == totalSupply()
