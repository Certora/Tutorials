methods {
    balanceOf(address) returns (uint256) envfree;
    totalSupply()      returns (uint256) envfree;
}

invariant totalSupplyBoundsBalance(address userA, address userB)
    balanceOf(userA) + balanceOf(userB) <= totalSupply()

// totalSupply is sum of balanceOf(user) for all users
ghost mathint sum_of_balances;

hook Sstore balances[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sum_of_balances = sum_of_balances + newValue - oldValue;
}

hook Sload uint v balances[KEY address user] STORAGE {
    require v == sum_of_balances;
}

invariant totalSupplyIsSumOfBalances()
    totalSupply() == sum_of_balances


