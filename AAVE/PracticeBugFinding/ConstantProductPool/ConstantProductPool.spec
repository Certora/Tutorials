
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
    require _token0 == token0();
    require _token1 == token1();
}

/*
Property: For both token0 and token1 the balance of the system is at least as much as the reserves.

This property is implemented as an invariant. 
Invariants are a specification of a condition that should always be true once an operation is concluded.
In addition, the invariant also checks that it holds right after the constructor of the code runs.

This invariant also catches a bug - TODO - understand the bug
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


/* write more rules as there are more bugs in the code */
