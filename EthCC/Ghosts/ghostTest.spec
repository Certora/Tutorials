ghost mapping(address => uint256) ghostBalance
{
    init_state axiom forall address a. ghostBalance[a] == 0;
}

// {
//     axiom forall address a. ghostBalance[a] > 0;
// }

hook Sload uint256 balance _balances[KEY address addr] STORAGE {
    require ghostBalance[addr] == balance;
}

hook Sstore _balances[KEY address addr] uint256 balance
    (uint256 old_balance) STORAGE
{
    ghostBalance[addr] = ghostBalance[addr] + balance - old_balance;
    totalSumGhost = totalSumGhost + balance - old_balance;
}

rule whoChangedBalance(env e, method f) {
    address user;

    uint256 ghostBalanceBefore = ghostBalance[user];
    uint256 balanceBefore = balanceOf(e, user);
    
    calldataarg args;
    f(e, args);

    uint256 ghostBalanceAfter = ghostBalance[user];
    uint256 balanceAfter = balanceOf(e, user);

    assert ghostBalanceBefore == ghostBalanceAfter, "Remember, with great power comes great responsibility.";
}



ghost uint256 totalSumGhost {
    init_state axiom totalSumGhost == 0;
}

ghost uint256 totalSupplyGhost
{
    init_state axiom totalSupplyGhost == 0;
}

hook Sload uint256 total _totalSupply STORAGE {
    require totalSupplyGhost == total;
}

hook Sstore _totalSupply uint256 total STORAGE {
    totalSupplyGhost = total;
}

invariant solvency()
    totalSumGhost == totalSupplyGhost




ghost mapping(address => mapping(address => uint256)) ghostAllowances
{
    init_state axiom forall address a. forall address b. ghostAllowances[a][b] == 0;
}

hook Sload uint256 alowance _allowances[KEY address owner][KEY address spender] STORAGE {
    require ghostAllowances[owner][spender] == alowance;
}

hook Sstore _allowances[KEY address owner][KEY address spender] uint256 alowance
    (uint256 old_alowance) STORAGE
{
    ghostAllowances[owner][spender] = ghostAllowances[owner][spender] + alowance - old_alowance;
}





// // AAVE-TOKEN-V3 example

// ghost mapping(address => uint256) ghostBalance
// {
//     init_state axiom forall address a. ghostBalance[a] == 0;
// }

// hook Sload uint104 balance _balances[KEY address addr].balance STORAGE {
//     require ghostBalance[addr] == balance;
// }

// hook Sstore _balances[KEY address addr].balance uint104 balance
//     (uint104 old_balance) STORAGE
// {
//     ghostBalance[addr] = ghostBalance[addr] + balance - old_balance;
// }

// rule whoChangedBalanceV3(env e, method f) {
//     address user;

//     uint256 ghostBalanceBefore = ghostBalance[user];
//     uint256 balanceBefore = balanceOf(e, user);
    
//     calldataarg args;
//     f(e, args);

//     uint256 ghostBalanceAfter = ghostBalance[user];
//     uint256 balanceAfter = balanceOf(e, user);

//     assert ghostBalanceBefore == ghostBalanceAfter, "Remember, with great power comes great responsibility.";
// }
