# Hints for ERC20

## General

A disclaimer before we begin - in all parametric rules that try to invoke the getters `name()` and `symbol()` you will get a violation. That happens because the way that the prover handles strings - basically a dynamic array. This representation forces the tool to use loops to handle this data type. Loops are a complex problem in the space of formal verification which we're going to explain and address in later lesson. For now just add the flag `--optimistic_loop` to the run command or shell script to mitigate this problem.


## ERC20Bug1.sol
<details>
<summary>Hint:</summary>
What are the values in the assertion that does not align correctly? Is it possible that the failing function got the final values to such relation?
</details>

</br>

## ERC20Bug2.sol
<details>
<summary>Hint 1:</summary>
How is it possible to overspend and in the same time gain funds?
</details>

</br>

<details>
<summary>Hint 2:</summary>
remember that code inside the <code>unchecked{}</code> isn't checked for overflow or underflow, so we need to check it manually
</details>

</br>

## ERC20Bug3.sol
<details>
<summary>Hint 1:</summary>
Is there anything in common to the 3 function that fail?
</details>

</br>

## ERC20Bug4.sol
<details>
<summary>Hint 1:</summary>
You've already fixed a similar bug on <code>ERC20Bug2.sol</code>
</details>

</br>

<details>
<summary>Hint 2:</summary>
Now that you've handled the underflow, is the allowance amount updates correctly?
</details>

</br>

## Rule `totalSupplyNotLessThanSingleUserBalance`
<details>
<summary>Hint 1:</summary>
Remember that the Certora Prover over-approximate, and so, if never told otherwise, it can start from infeasible states.
</details>

</br>

<details>
<summary>Hint 2:</summary>
Note what is the initial `totalSupply`, `balanceBefore`, and what is the balance of the user from which the `transfer` is being made. Does the sum of the 2 balances really sum up to `totalSupply`?
</details>
