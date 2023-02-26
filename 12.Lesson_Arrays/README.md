# Reasoning over arrays
In this chapter we will review the pitfalls and different methods verifying
invariants over array.

## 1. Basic
Here we show that taking a naive approach will often fail.
Consider the `Array` contract in [Array.sol](1.Basic/Array.sol), and its
specification in [Array.spec](1.Basic/Array.spec).

1. The `uniqueArray` invariant (in [Array.spec](1.Basic/Array.spec))
   verifies on the `push()` method. However, the `push()` method does not
   ensure the elements in `arrOfTokens` are unique.
   Do you understand why the invariant held - what is the mistake?
   <details>
   <summary>Hint. </summary>

   Recall that by default the Prover ignores reverting paths.

   </details>
1. On the other hand, the `uniqueArrayUsingRevert` invariant fails to verify,
   but its failure is unrelated to the solidity code in
   [Array.sol](1.Basic/Array.sol). Indeed this invariant is useless, do you
   understand why?
   <details>
   <summary>Hint.</summary>

   What is the value of `get@withrevert(i)` when the function does revert?

   </details>
1. Fix the `uniqueArray` invariant so it correctly verifies that elements in
   the array are unique (except perhaps for `address(0)`). Check that the new
   invariant indeed fails on the `push()` method.
   <details>
   <summary>Hint.</summary>

   Use `getWithDefaultValue` method. A solution can be found in
   [ArraySemiFixed.spec](../Solutions/12.Lesson_Arrays/1.Basic/ArraySemiFixed.spec).

   </details>
1. A partial fix to the solidity code in [Array.sol](1.Basic/Array.sol) is found
   in [ArrayImproved.sol](1.Basic/ArrayImproved.sol). There, the code prevents
   pushing the same address twice, using a mapping indicating which addresses
   were pushed. Modify the `uniqueArray` invariant, and add additional invariants,
   so `uniqueArray` is verified on [ArrayImproved.sol](1.Basic/ArrayImproved.sol).
   <details>
   <summary>Solution.</summary>
   
   See [Array.spec](../Solutions/12.Lesson_Arrays/1.Basic/Array.spec).

   </details>

## 2. Intermediate
Take a look in [ArrayUniqueBug.sol](2.Intermediate/ArrayUniqueBug.sol). Here
the contract maintains a unique array of addresses by ensuring that the address
to be pushed is not already in the array. We will see how to write invariants for
this pattern.

1. The contract `ArrayUniqueBug` (from
   [ArrayUniqueBug.sol](2.Intermediate/ArrayUniqueBug.sol)) has bugs. It allows the
   array to become non-unique. Fix the contract by requiring `frequence(value) == 0`
   in the appropriate places. Save the fixed contract as `ArraySolution.sol` and name
   the contract `ArraySolution`.
1. The `uniqueArray` invariant in
   [ArrayUniqueBug.spec](2.Intermediate/ArrayUniqueBug.spec) will identify the buggy
   methods in [ArrayUniqueBug.sol](2.Intermediate/ArrayUniqueBug.sol). However,
   it will still fail on correct methods in `ArraySolution` (e.g. `swap(uint256,uint256)`).
   Fix the `uniqueArray` invariant, by using `requireInvariant`. Verify that
   `ArraySolution` passes without violation, while `ArrayUniqueBug` still fails.
   <details>
   <summary>Hint.</summary>

   You must ensure that `frequency` does not get too high.

   </details>
