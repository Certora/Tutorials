using Asset_ERC20 as underlying


methods
{
    // pool mathematical function
    amountToShares(uint256 amount) returns (uint256) envfree    
    sharesToAmount(uint256 shares) returns (uint256) envfree    
    calcPremium(uint256 amount) returns (uint256) envfree 
    feeRate() returns (uint256) envfree   

    totalSupply() returns(uint256) envfree

    //erc20 function for calling from spec
    underlying.balanceOf(address) returns(uint256) envfree
}

function poolBalance() returns uint256 {
    return underlying.balanceOf(currentContract); 
}

/* 
    calcPremium properties:
        a. max value: calcPremium(x) < x    where x!=0
        b. monotonicity: x < y => calcPremium(x) <= calcPremium(y)
*/
rule integrityOfCalcPremium(uint x, uint y) {
    require( feeRate() < 100); //safe assumption 
    assert x > 0 => calcPremium(x) < x; 
    assert x < y => calcPremium(x) <= calcPremium(y); 
}     


/*
    amountToShares and sharesToAmount properties:
        a. zero value
            amountToShares(0) = sharesToAmount(0) = 0
        b. monotonicity  
            i.  x < y => amountToShares(x) <= amountToShares(y)
            ii. x < y => sharesToAmount(x) <= sharesToAmount(y)  
        c. inverse (up to roundig error)
            i. sharesToAmount(amountToShares(x)) ~= x
            ii. amountToShares(sharesToAmount(x)) ~= x
        d. ratio
            totSupply / balanceOf  =  

*/

// mathematical properties and also unit tests

rule monotonicity_amountToShares(uint x, uint y) {
    assert  x < y => amountToShares(x) <= amountToShares(y);
    assert amountToShares(0) == 0;
}

rule monotonicity_sharesToAmount(uint x, uint y) {
    assert  x < y => sharesToAmount(x) <= sharesToAmount(y);
    assert sharesToAmount(0) == 0;
}



rule inverse_amount(uint x) {
    uint shares = amountToShares(x);        
    uint backToAmount = sharesToAmount(shares);
    uint twoShareValue = mul(2,poolBalance() / totalSupply());
    uint twoAmountValue = mul(2,totalSupply() / poolBalance())  ;
    assert( (x - twoShareValue - twoAmountValue) <= backToAmount && backToAmount <= x  );
}

rule inverse_shares(uint x) {
    uint amount = sharesToAmount(x);
    uint backToShares = amountToShares(amount);
    uint twoShareValue = mul(2,poolBalance() / totalSupply());
    uint twoAmountValue = mul(2,totalSupply() / poolBalance());
    assert( (x - twoShareValue - twoAmountValue) <= backToShares && backToShares <= x);
}




	function mul(uint256 a, uint256 b) returns uint256 {
		if (a == 0 || b == 0) {
			return to_uint256(0);
		}
		
		uint256 c = to_uint256(a * b);
		require b ==(c / a);
		
		return c;
	}