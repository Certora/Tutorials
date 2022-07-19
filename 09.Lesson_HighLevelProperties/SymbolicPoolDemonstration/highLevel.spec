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

    // for checing call backs to the pool's function
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
        The total supply of the system is less than or equal to the underlying asset holdings of the system
    */
    invariant totalSupply_LE_balance()
	    totalSupply() <= underlying.balanceOf(currentContract)
        {
            preserved with(env e) {
                require e.msg.sender != currentContract;
            }
        }
	
    /*
        The total supply of the system is zero if and only if the balance of the system is zero
    */
	invariant totalSupply_vs_balance()
		totalSupply() == 0 <=> underlying.balanceOf(currentContract) == 0
		{
			preserved with(env e) {
				require e.msg.sender != currentContract;
			}
		}
	
	rule deposit_GR_zero() {
		// failing due to bugs in the code
		env e;
		require e.msg.sender != currentContract;
		
		uint256 amount;
		uint256 amountMinted = deposit(e, amount);
		
		assert amount > 0 <=> amountMinted > 0;
	}
	
	rule more_user_shares_less_underlying(method f) // failures need to check
	filtered {
		f -> f.selector != flashLoan(address, uint256).selector  && 
            f.selector != transfer(address, uint256).selector && f.selector != transferFrom(address, address, uint256).selector && !f.isView
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
	
	rule more_shares_more_withdraw() {
		// failing
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
		require poolBalance1 == supply1;

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
	
	function global_requires(env e) {
		require e.msg.sender != currentContract;
		require e.msg.sender != flashLoanReceiver;
		requireInvariant totalSupply_vs_balance();
		requireInvariant totalSupply_LE_balance();
	}
	
	
