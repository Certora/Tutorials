methods{
    getTotalSupply() returns(uint256) envfree
}

ghost uint256 sumOfBalances{
    init_state axiom sumOfBalances == 0;
}

hook Sstore balances[KEY address key] uint256 newValue (uint256 oldValue) STORAGE {
    sumOfBalances = sumOfBalances + newValue - oldValue;
}


invariant sum()
    sumOfBalances == getTotalSupply()

