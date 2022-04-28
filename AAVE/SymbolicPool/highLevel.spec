using Asset_ERC20 as underlying
using SymbolicFlashLoanReceiver as flashLoanReceiver

 methods
{
    // pool's erc20 function
    balanceOf(address) returns(uint256) envfree
    totalSupply() returns(uint256) envfree
    // pools additional envfree functions
    amountToShares(uint256 amount) returns (uint256) envfree    
    sharesToAmount(uint256 amount) returns (uint256) envfree    
    calcPremium(uint256 amount) returns (uint256) envfree    

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

	// getter for a public variable
	_balanceOf(address) returns (uint256)
 
}

function global_requires(env e) {
	require e.msg.sender != currentContract;
	require e.msg.sender != flashLoanReceiver;
	requireInvariant totalSupply_vs_balance();
	requireInvariant totalSupply_LE_balance();
}


// accumulator for userBalances
ghost mathint sumUserBalances {
    init_state axiom sumUserBalances == 0;
}


// sumUserBalances is updated on each user balance change
// can use a hook on private variable
hook Sstore _balanceOf[KEY address user] uint256 balance
    (uint256 old_balance) STORAGE {
        sumUserBalances = sumUserBalances + to_mathint(balance) - to_mathint(old_balance);
}

/*
	Sum of all the user balances equals exactly to token (pool token) total supply.

	Formula:
	{
		Sum(balance(user)) = totalSupply()
	}
*/
invariant userBalancesAreTotalSupply()
	to_mathint(totalSupply()) == sumUserBalances
	

/*
	The total supply of the system is less than equal the underlying assert holding of the system.
	
	Formula:
	{
		totalSupply() <= underlying.balanceOf(this)
	}
*/
invariant totalSupply_LE_balance()
	totalSupply() <= underlying.balanceOf(currentContract)
	
	// without this preserved block we have a counterexample:
	// the pool itself deposits its underlying token to itself.
	// as a result the balance of underlying doesn't change but totalSupply() grows 
	{
		preserved with(env e) {
			require e.msg.sender != currentContract;
		}
	}

/*
	The total supply of the system is zero if and only if the balanceof the system is zero

	Formula:
	{
		totalSupply() == 0 <=> underlying.balanceOf(this) == 0
	}
*/
invariant totalSupply_vs_balance()
	totalSupply() == 0 <=> underlying.balanceOf(currentContract) == 0
	{
		preserved with(env e) {
			require e.msg.sender != currentContract;
		}
	}

/*
	Pool tokens are minted if and only if deposit is non-zero

	Formula:
	{
		msg.sender != this;
	}
	<
		amountMinted = deposit(amount);
	>
	{
		amount > 0 <=> amountMinted > 0
	}
*/
rule deposit_GR_zero() {
	env e;
	require e.msg.sender != currentContract;
	
	uint256 amount;
	uint256 amountMinted = deposit(e, amount);
	
	assert amount > 0 <=> amountMinted > 0;
}

/* 
    State Transition: when a user become an LP provider 
	Formula:
	{
		isLPproviderBefore = balanceOf(msg.sender) > 0
	} 
	<
		f(e, args)
	>
	{
		isLPproviderAfter = balanceOf(msg.sender)
		f.selector == deposit => isLPproviderAfter;
		f.selector == withdraw => isLPproviderBefore;
	}
*/
rule changeLpProvider(address user, method f) {
    env e;
    calldataarg args;
    require e.msg.sender == user;

    bool isLPproviderBefore = balanceOf(user) > 0 ;
    
	f(e,args);
    
    bool isLPproviderAfter = balanceOf(user) > 0 ;
    assert f.selector == deposit(uint256).selector => isLPproviderAfter;
    assert f.selector == withdraw(uint256).selector => isLPproviderBefore; 
}

/*
    Variable Transition : totalSupply can only change on deposit and withdraw
	Formula:
	{
		before = totalSupply()
	}
	<
		f(e, args)
	>
	{
		after = totalSupply()
		after > before => f.selector == deposit
		after < before => f.selector == withdraw
	}
*/
rule changeTotalSupply(method f) {
    uint256 before = totalSupply() ;
    env e;
	require e.msg.sender != currentContract;
    calldataarg args;
    uint256 amount;

	f(e,args);
    
    uint256 after = totalSupply() ;
    assert after > before <=> f.selector == deposit(uint256).selector; 
    assert after < before <=> f.selector == withdraw(uint256).selector;  
}

/*
    Risk : a user can not withdraw twice
	Formula:

	{
		amount = balanceOf(msg.sender)
	}
	<
		withdraw(amount);
		withdraw(amount;)
	{
		second withdraw call reverts
	}
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


/*
	Caller's balance of underlying is inversely correlated with the pool token balance
	
	Formula:
	{
		underlying_balance_before = underlying.balanceOf(msg.sender)
		balance_before = balanceOf(msg.sender)
	}
	<
		f(e, args)
		underlying_balance_after = underlying.balanceOf(msg.sender)
		balance_after = balanceOf(msg.sender)
	>
	{
		balance_after > balance_before <=> underlying_balance_after < underlying_balance_before
		balance_after < balance_before <=> underlying_balance_after > underlying_balance_before
	}

*/
rule more_user_shares_less_underlying(method f) 
filtered {
	f -> f.selector != flashLoan(address, uint256).selector  && 
		f.selector != transfer(address, uint256).selector && 
		f.selector != transferFrom(address, address, uint256).selector && !f.isView
}
{
	env e;
	
	uint256 Underlying_balance_before = underlying.balanceOf(e.msg.sender);
	uint256 User_balance_before = balanceOf(e.msg.sender);
	
	global_requires(e);
	
	calldataarg args;
	f(e, args);
	
	uint256 Underlying_balance_after = underlying.balanceOf(e.msg.sender);
	uint256 User_balance_after = balanceOf(e.msg.sender);
	
	assert User_balance_after > User_balance_before <=> Underlying_balance_after < Underlying_balance_before;
	assert User_balance_after < User_balance_before <=> Underlying_balance_after > Underlying_balance_before;
}

/*
	Greater amount of shares => greater amount of withdrawn underlying token

	Formula:
	{
		storage init = lastStorage
	}
	<
		amountX = withdraw(sharesX)
		amountY = withdraw(sharesY) at init
	>
	{
		sharesX > sharesY => amountX => amountY
	}
*/
rule more_shares_more_withdraw() {
	env e;
	
	uint256 sharesX;
	uint256 sharesY;
	uint256 amountX;
	uint256 amountY;
	
	global_requires(e);
	
	storage init = lastStorage;
	
	amountX = withdraw(e, sharesX);
	amountY = withdraw(e, sharesY) at init;
	
	assert sharesX > sharesY => amountX >= amountY;
}

/*
	Flashloan can only add value to the pool.
	{
		totalSupply_pre = totalSupply()
		balance_pre = underlying.balanceOf(this)
		flashloanReceiver.callBackOption = 0
	}
	<
		flashloan(receiver, amount)
	>
	{
		totalSupply_post = totalSupply()
		balance_post = underlying.balanceOf(this)
		balance_post > balance_pre
	}
*/
rule flashLoan_adds_value(address receiver, uint256 amount) {
	env e;
	
	global_requires(e);
	uint256 totalSupply_pre = totalSupply();
	uint256 balance_pre = underlying.balanceOf(currentContract);
	flashLoan(e, receiver, amount);
	uint256 totalSupply_post = totalSupply();
	uint256 balance_post = underlying.balanceOf(currentContract);
	
	assert flashLoanReceiver.callBackOption(e) == 0 => balance_post > balance_pre;
	assert balance_post * totalSupply_pre >= balance_pre * totalSupply_post;
}


/*
	User doesn't lose funds from a flashloan
*/
rule user_solvency_on_flashLoan(address user) {
	env e;
	
	require user != currentContract && user != flashLoanReceiver.to(e) && user != flashLoanReceiver;
	global_requires(e);
	
	uint256 shares_pre = balanceOf(user);
	uint256 poolBalance1 = underlying.balanceOf(currentContract);
	uint256 supply1 = totalSupply();
	mathint withdrawableAmount1 = sharesToAmount(shares_pre);
	uint256 userBalance1 = underlying.balanceOf(user);
	mathint total_pre = withdrawableAmount1 + userBalance1;
	require shares_pre <= supply1; 

	uint256 amount;
	uint256 premium = calcPremium(amount);
	flashLoan(e, flashLoanReceiver, amount);
	
	uint256 shares_post = balanceOf(user);
	uint256 poolBalance2 = underlying.balanceOf(currentContract);
	uint256 supply2 = totalSupply();
	
	mathint withdrawableAmount2 = sharesToAmount(shares_post);
	uint256 userBalance2 = underlying.balanceOf(user);
	mathint total_post = withdrawableAmount2 + userBalance2;
	
	
	assert(user != e.msg.sender && shares_pre != 0) =>(total_pre <= total_post  && total_post <= total_pre + premium);
	assert(user == e.msg.sender && shares_pre != 0) =>( total_post <= total_pre  && total_pre <= total_post + premium);
	assert(user != e.msg.sender && shares_pre == 0) =>(total_pre == total_post);
	assert(user == e.msg.sender && shares_pre == 0) =>( total_post == total_pre - premium );
}

/*
	User doesn't lose funds on method calls which are not a flashloan
*/
rule user_solvency_without_flashloan(address user, method f) filtered {
	f -> f.selector != flashLoan(address,uint256).selector  &&  
		f.selector != transferFrom(address, address, uint256).selector
}
{
	env e;
	require user != currentContract && user != flashLoanReceiver;
	global_requires(e);
	
	uint256 poolBalance1 = underlying.balanceOf(currentContract);
	uint256 supply1 = totalSupply();
	
	uint256 shares_pre = balanceOf(user);
	require shares_pre <= totalSupply();
	uint256 withdrawableAmount_pre = sharesToAmount(shares_pre);
	uint256 userBalance_pre = underlying.balanceOf(user);
	mathint total_pre = withdrawableAmount_pre + userBalance_pre;
	
	calldataarg args;
	f(e, args);
	
	uint256 shares_post = balanceOf(user);
	uint256 withdrawableAmount_post = sharesToAmount(shares_post);
	uint256 userBalance_post = underlying.balanceOf(user);
	mathint total_post = withdrawableAmount_post + userBalance_post;
	
	assert(e.msg.sender == user) => total_pre >= total_post;
	assert(e.msg.sender != user) => total_pre <= total_post;
}
