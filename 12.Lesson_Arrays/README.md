# Reasoning over arrays
In this chapter we will review the pitfalls and different methods of handling arrays.

## 1. Basic
Consider the `Array` contract in [Array.sol](1.Basic/Array.sol), and its
specification in [Array.spec](1.Basic/Array.spec).

1. The `uniqueArray` invariant (in [Array.spec](1.Basic/Array.spec))
   verifies on the `push()` method. However, the `push()` method does not
   ensure the elements in `arrOfTokens` are unique.
   Do you understand why the invariant held - what is the mistake?
   <details><summary>Hint. </summary>
   Recall that by default the Prover ignores reverting paths.
   </details>
1. On the other hand, the `uniqueArrayUsingRevert` invariant fails to verify,
   but its failure is unrelated to the solidity code in
   [Array.sol](1.Basic/Array.sol). Indeed this invariant is useless, do you
   understand why?
   <details>
   <summary>**Hint.**</summary>

   What is the value of `get@withrevert(i)` when the function does revert?

   </details>
1. Fix the `uniqueArray` invariant so it correctly verifies that elements in
   the array are unique (except perhaps for `address(0)`). Check that the new
   invariant indeed fails on the `push()` method.
   <details><summary>Hint.</summary>
   Use `getWithDefaultValue` method. A solution can be found in
   [ArraySemiFixed.spec](../Solutions/12.Lesson_Arrays/1.Basic/ArraySemiFixed.spec).
   </details>
1. A partial fix to the solidity code in [Array.sol](1.Basic/Array.sol) is found
   in [ArrayImproved.sol](1.Basic/ArrayImproved.sol). There, the code prevents
   pushing the same address twice, using a mapping indicating which addresses
   were pushed. Modify the `uniqueArray` invariant, and add additional invariants,
   so `uniqueArray` is verified on [ArrayImproved.sol](1.Basic/ArrayImproved.sol).
   <details><summary>Solution.</summary>
   See
   [Array.spec](../Solutions/12.Lesson_Arrays/1.Basic/Array.spec).
   </details>

- Make sure your rules detect the error on ArrayWrong.sol 
- Prove that `frequency(address value)` returns maximum 1 for any non-zero value; Show that it
  fails on zero values.

