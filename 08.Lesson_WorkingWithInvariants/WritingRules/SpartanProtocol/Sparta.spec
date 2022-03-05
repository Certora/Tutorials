methods {
    // sparta functions
    init_pool()
    add_liquidity()
    remove_liquidity(uint256)
    swap(address) 
    sync() envfree
    getContractAddress()  returns (address) envfree
    getToken0DepositAddress()  returns (address) envfree
    getToken1DepositAddress() returns (address) envfree

    // my utility functions
    getK() returns (uint256) envfree
    myAddress() returns (address) envfree
    getTokenBalance(address, address) envfree
    getBalance(address) returns(uint256) envfree
    
    // erc20 functions
    totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    getAllowance(address, address) returns (uint256) envfree
    approve(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)
    increase_allowance(address, uint256)
    decrease_allowance(address, uint256)
}

/*
Option 1 - In remove liquidity sync the pool actual and recorded balances. 
Option 2 - In remove liquidity require that the actual and recorded balances are the same. 
Option 3 - In remove liquidity calculate the amount of tokens to transfer using the recorded balance instead of the actual.
add liquidity, liquidity added
remove liquidity, liquidity removed
*/

// ***Unit test*** - swapping token0 works properly
rule properlyWorkingSwap0(address from, address to) {
    env e;
    address token0 = getToken0DepositAddress();
    address token1 = getToken1DepositAddress();
    uint256 balance0Before = getTokenBalance(token0, e.msg.sender);
    uint256 balance1Before = getTokenBalance(token1, e.msg.sender);
    swap(e, token0);
    uint256 balance0After = getTokenBalance(token0, e.msg.sender);
    uint256 balance1After = getTokenBalance(token1, e.msg.sender);
    assert ((balance1After - balance1Before) >= 0, "token1 balance decreased");
    assert (balance0After == 0, "not all token0 balance was transferred");
}

// ***Unit test*** - swapping token1 works properly
rule properlyWorkingSwap1(address from, address to) {
    env e;
    address token0 = getToken0DepositAddress();
    address token1 = getToken1DepositAddress();
    uint256 balance0Before = getTokenBalance(token0, e.msg.sender);
    uint256 balance1Before = getTokenBalance(token1, e.msg.sender);
    swap(e, token1);
    uint256 balance0After = getTokenBalance(token0, e.msg.sender);
    uint256 balance1After = getTokenBalance(token1, e.msg.sender);
    assert ((balance0After - balance0Before) >= 0, "token1 balance decreased");
    assert (balance1After == 0, "not all token0 balance was transferred");
}

// ***Variable transition*** - constant product of tokens amount are maintained
rule constantK(method f) {
    env e;
    calldataarg args;

    uint256 KBefore = getK();
    swap(e, args);
    uint256 KAfter = getK();

    assert KAfter == KBefore, "K changed";
}

// ***Valid state*** - contract is never drained
//rule contractNotDrained(method f, method g, method h) {
    //any account that interacts with the contract should only be able to touch the funds they has in the system before they itneracted with it.
//}