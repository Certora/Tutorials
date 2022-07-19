# Hints for Borda system
## BordaBug1.sol
<details>
<summary>Hint:</summary>
Look at the description of the voting mechanism in IBorda.sol, what is the failing assert? does the values of the contenders' points make sense?
</details>

</br>

## BordaBug2.sol
<details>
<summary>Hint:</summary>
Check again the requirements in the failing function. Does it seem right?
</details>

</br>

## BordaBug3.sol
<details>
<summary>Hint 1:</summary>
What assert is failing? What are the values that cause the (in)equalities to break? Does it make sense that addition of points will decrease the count?
</details>

</br>

<details>
<summary>Hint 2:</summary>
Remember that we added the <code>SafeMath()</code> library for a reason.
</details>

</br>

## BordaBug4.sol
<details>
<summary>Hint:</summary>
Go over the failing function again. Remember, once a voter has registered should be registered for life. If the voter is blacklisted he shall be punished financially in the future. 
</details>
