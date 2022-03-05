# Properties

***Valid states***

***State transitions***

***Variable transitions***

1. non reverting add_liquidity called with nonzero changes in balance <=> K, totalSupply and sender balance increases
2. non reverting remove_liquidity called with nonzero changes in balance <=> K, totalSupply and sender balance decreases
3. k constant unless add_liquidity or remove_liquidity was called

***High-level properties***

4. init_pool() can be called only once
5. swap() should maintain K
6. swap(token0) increases balance0 and decreases balance1
7. total supply =! 0 <=> balance0 != 0 and balance1 != 0
8. total supply == sum of all user balances
9. total supply >= any user balance

***Unit tests***

10. all state changing functions

# Priority

## High

all high, can break the system

## Medium

## Low
