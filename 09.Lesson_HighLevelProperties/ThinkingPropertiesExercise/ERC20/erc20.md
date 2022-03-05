# Properties

***Valid states***

***State transitions***

***Variable transitions***

1. balance is changed => transfer/transferFrom called
2. TransferFrom decreases allowance of msg.sender

***High-level properties***

3. total allowance == sum of all allowances
4. supply only changes on burn and mint ( _transfer doesnt change supply)
5. totalSupply == sum of all users' balance
6. Transfer only effects balance of two users involved (sender, receiver)
7. balanceOf(user) <= totalSupply()
8. sum of all user balances == totalSupply

***Unit tests***
9. all state changing functions

# Priority

## High

1, 2, 5, 6, 7, 8

## Medium

3, 4,

## Low
