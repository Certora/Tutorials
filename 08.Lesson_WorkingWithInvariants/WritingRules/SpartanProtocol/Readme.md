## Spartan Protocol Bug
The spartan protocol is a pool that allows users to swap between two tokens – BASE and TOKEN. The swap rates are maintained by AMM and there are some stability optimization for the benefit of the liquidity providers.
Spartan protocol has been hacked for 30M$ of liquidity providers funds. The bug isn’t at one specific function – but rather the use of two functions, addLiquidity and removeLiquidity, led to a bug that allows the attacker to drain the pool funds. 
This summary explains the two functions logic, and then how the attacker exploited it.

### addLiquidity:
1. Transfer tokens to spartan account.
2. Then the difference between the current spartan account tokens amount to the tokens amount recorded before the transfer is the transferred amount, mint LP token for this amount.

If 1 and 2 happens in different transactions, then the transferred tokens can be use by another account that also added liquidity and its transaction took place between 1 and 2. The correctness holds only if 1+2 are done at one transaction.

### removeLiquidity:
1. Calculate LP token worth by calculating the portion of the those LP token from the total LP tokens and multiply by current pool balance.
2. Burn the tokens and pay this amount.

### The bug:
We explain the bug by showing a simplified version of the actual attack. Suppose at the starting point of the transaction the pool balance is B, and there are K liquidity provider tokens minted. 

![alt text](img/table.png)

The attacker ends with total cash amount of 2.5B where at the beginning he had 2B of cash. All of those steps must happen at the same transaction.

### How to fix the bug
Option 1 - In remove liquidity sync the pool actual and recorded balances. 
Option 2 - In remove liquidity require that the actual and recorded balances are the same.
Option 3 - In remove liquidity calculate the amount of tokens to transfer using the recorded balance instead of the actual.

## How to perform the attack
Open the code in Remix IDE and perform the following steps:

1. Deploy 2 instances of MyToken - token0, token1.
2. Deploy SpartanPool where token0 and token1 are the cotracts addresses deployed at step 1.
3. Deposit 10 ether to token0 and another 10 ether to token1.
4. Transfer the 10 ether to the pool in both token0 and token1 (token0.transfer(pool_address, 1000000000), token1.transfer(pool_address, 1000000000)).
5. Press init_pool() at the pool contract.
6. Switch user. [to user2]
7. Deposit 16 ether to token0 and another 16 ether to token1.
8. Transfer the 8 ether to the pool in both token0 and token1.
9. Press add_liquidity() at the pool contract.
10. Transfer the left 8 ether to the pool in both token0 and token1.
11. Press remove_liquidity(80000) at the pool contract.
12. Press add_liquidity() at the pool contract.
13. Press remove_liquidity(124137) at the pool contract.
14. Press withdraw() at token0 and token1 contracts.

Steps 1-5 are used to build the pool. The actual attack happens at 6-14 and the attacker is user2 (the user we switched to) which ends with 7 ether more than had at step 6.
