# Properties For SymbolicPool

We took some time to study the system, ask questions, discuss with each other on the way it operates and came up with the following properties:

1. ***Variable transitions*** - `balanceOf(user)` increases => `deposit()` function was called. If any other function increase the balance of the the system then the contract doesn’t work as intended (assuming no external transfers are made to the user).

2. ***Variable transitions*** - `balanceOf(user)` decreases => `withdraw()` function was called. If any other function decrease the balance of the the system then the contract doesn’t work as intended (assuming no external transfers are made to the user).

3. ***High-level*** - `totalSupply()` of the system is less than or equal to the `asset.balanceOf(address(this))` - each LP token represent at least 1 underlying token (number of shares <= number of underlying tokens).

4. ***Valid state*** - The totalSupply of the system is zero if and only if the underlying balance of the system is zero:
    1. if there are LP tokens, then there are underlying tokens in the contract.
    2. if there are no LP tokens, then there are no underlying tokens in the contract.
    ```cvl
    totalSupply() == 0 <=> asset.balanceOf(address(this)) == 0
    ```

5. ***High-level*** - If deposited more than 0 underlying tokens, then minted more than 0 and LP tokens vice versa - depositing non-zero amount of underlying in the pool must mint LP tokens.

6. ***High-level*** - Solvency of the system - the system has enough money to pay everyone.

    1. The totalSupply of the pool is greater or equal to the sum of balances of all users - <span style="color:red"> That refers to LP tokens. We want to make sure that the system always have enough LP tokens to back what it owes to the users.</span>

    2. ```cvl
        asset.balanceOf(address(this)) >= sum of sharesToAmount(balanceOf(user))
        ```
    <span style="color:red"> That refers to the underlying underlying tokens. We want to make sure that the system always have the funds to pay to the user what it owes him/her. The amount of underlying underlying in the system is at least equal to the worth of the LP tokens in terms of underlying token. </span>

7. ***High-level*** - The more shares you have, the more you can withdraw (can be equal because of division) - A simple but strong property

8. ***High-level*** - No frontrunning - one user’s action should not affect another user’s action.

9. ***Unit tests*** - integrity of deposit - calling `deposit()` increases `totalSupply()`, `balanceOf(user)`, `asset.balanceOf(address(this))` and decreases `asset.balanceOf(user)` by `amount`.

10. ***Unit tests*** - integrity of withdraw - `withdraw()` decreases `totalSupply()`, `balanceOf(user)`, `asset.balanceOf(address(this))` and increases `asset.balanceOf(user)` by `shares`.

</br>

---

## Prioritizing

</br>

Once the list of properties is finished, the team meet to discuss it. Each property is explained by its creator to the others, and either being approved, denied or refined.
With every property the team discuss the implications of the property failing, and prioritize them accordingly.

Here is a summary of our prioritization:

### High Priority:

- Property 3 is high priority since it promises that a user can withdraw his deserved funds without any lock of assets.
If 1 underlying token was to be represented by multiple LP tokens (say 2), then burning 1 LP token at a time could've see a user burning all its LP tokens, while getting non of its deserved funds. This money would be unreachable by any one.

- Properties 4 & 5 are quite similar, and are high priority since if they fail that means that the correlation between LP tokens and underlying tokens are corrupted, i.e. LP tokens aren't being minted at deposit properly, and/or aren't being burned properly at withdraw.

- Property 6 is high priority since if is checking of solvency. We expect that the system always have access to all the money that it owes its users. If this system can lose its solvency, there's nothing that promise to the users that they will get their deserved money back.

- Property 7 is high priority since it is a fundamental idea in a liquidity pool - LP tokens represent shares in the pool, and the more shares one have the more underlying token they should receive upon withdrawal.

- Property 8 is high priority since if one user could've affect another user's actions by calling a function from within the contract legitimately, then the first would've been able to attack the second in different ways - DoS, steal his/her funds, etc.

### Medium Priority:

- Properties 1 & 2 are medium priority since
    they check the behavior of the system with respect to any action that can be made in the contract (they how every function behave and categorize them).

### Low Priority:

- Properties 9 & 10 are low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.