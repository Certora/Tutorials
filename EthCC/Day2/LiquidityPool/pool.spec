using Asset_ERC20 as underlying
using SymbolicFlashLoanReceiver as flashLoanReceiver

methods
{
    // pool's erc20 function
    balanceOf(address) returns(uint256) envfree
    totalSupply() returns(uint256) envfree
    // for checking call backs to the pool's function
    deposit(uint256) returns(uint256)  => DISPATCHER(true)
    withdraw(uint256) returns (uint256)  => DISPATCHER(true)
    flashLoan(address, uint256)  => DISPATCHER(true)
   
    // flash loan receiver function
    executeOperation(uint256,uint256,address) => DISPATCHER(true)
    //erc20 function
    transfer(address, uint256) returns (bool) => DISPATCHER(true)
    transferFrom(address, address, uint256) returns (bool) => DISPATCHER(true)
    //erc20 function for calling from spec
    underlying.balanceOf(address) returns(uint256) envfree
 
}

/*
    Unit Test: integrity of withdraw  - updates balanceOf as expected
*/
rule integrityOfWithdraw(address user, uint256 amount) {
    uint before = balanceOf(user);
    env e;
    require e.msg.sender == user;
    withdraw(e, amount);
    assert balanceOf(user) == before - amount;
} 

/* 
    Valid State: The balance of user is less than the total supply
    Proving this by proving a stronger property the sum of all balances equal totalsupply 
*/
ghost sumAllBalances() returns mathint {
	init_state axiom sumAllBalances()==0; 
}


hook Sstore _balanceOf[KEY address a] uint256 balance
// the old value ↓ already there
    (uint256 old_balance) STORAGE {
  havoc sumAllBalances assuming sumAllBalances@new() == sumAllBalances@old() +
      balance - old_balance;
}

invariant balance_SE_supply(address user)
    sumAllBalances() == totalSupply()
   
/* 
    State Transition: when a user become an LP provider  
*/
rule changeLpProvider(address user, method f) {
    env e;
    calldataarg args;
    require e.msg.sender == user;
    uint256 amount;
    require amount > 0; 

    bool isLPproviderBefore = balanceOf(user) > 0 ;
    

    if(f.selector == deposit(uint256).selector)
        deposit(e, amount);
    else if(f.selector == withdraw(uint256).selector)
        withdraw(e, amount);
    else    
        f(e,args);
    
    bool isLPproviderAfter = balanceOf(user) > 0 ;
    assert f.selector == deposit(uint256).selector => isLPproviderAfter;
    assert f.selector == withdraw(uint256).selector => isLPproviderBefore; 
}

/*
    Variable Transition : totalSupply can only change on deposit and withdraw
*/
rule changeTotalSupply(method f) {
    uint256 before = totalSupply() ;
    env e;
    calldataarg args;
    uint256 amount;
    if(f.selector == deposit(uint256).selector)
        deposit(e, amount);
    else if(f.selector == withdraw(uint256).selector)
        withdraw(e, amount);
    else    
        f(e,args);
    
    uint256 after = totalSupply() ;
    assert after > before <=> ( f.selector == deposit(uint256).selector && amount > 0) ; 
    assert after < before <=> ( f.selector == withdraw(uint256).selector && amount > 0) ;  
}

/*
    High Level : The total supply of the system is less than equal the underlying assert holding of the system
*/
invariant totalSupply_LE_balance()
    totalSupply() <= underlying.balanceOf(currentContract)
    {
        preserved with(env e) {
            require e.msg.sender != currentContract;
        }
    }

/*
    Risk : a user can not withdraw twice
*/
rule noDoubleWithdraw(address user) {
    uint256 amount = balanceOf(user);
    env e;
    require e.msg.sender == user;
    withdraw(e, amount);
    uint256 x;
    withdraw@withrevert(e,x);
    assert lastReverted; 
}


add more ides to here:
https://docs.google.com/document/d/14kQOZINtlZxf_br_k5CCJeAhaJtADO9sHVBtxgf7daA/edit# 
