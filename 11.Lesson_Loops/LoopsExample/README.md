# Loop Example

In this example we will play with the flags `--optimistic_loop` and `--loop_iter`, and see how different settings for handling loops can change the verification result of the exact same rule on the exact same function.

- [ ] Have a look at [Loops.sol](Loops.sol) and [LoopsUnrolling.spec](LoopsUnrolling.spec)

- [ ] Run the `.spec` file with the script [verifyLoops.sh](verifyLoops.sh) and see the results.

<details>
  <summary>Question: Do you understand why all 4 rules fail?</summary>
  Answer: All 4 rules fail because they run with the default pessimistic loop. It assumes that the loop got unrolled more times than it should. 
</details>

</br>

- [ ] If we were to add `--optimistic_loop` flag to `slow_copy_correct`, can you predict what the results would be?
Change the script and check your prediction.

<details>
  <summary>Question: Do you understand why this rule passed?</summary>
  Answer: This rule is basically true. Assuming that the loop being unrolled fully the returned value should always be `n`. The `--optimistic_loop` flag required `n` to fit the number of times the loop is  unrolled (i.e. `require(!(i < n))`). In our case, since we didn't set the `--loop_iter` its value is default (1), so the requirement force `n = 1`.
</details>

</br>

- [ ] If we were to add `--optimistic_loop` flag to `slow_copy_wrong`, can you predict what the results would be?
Change the script and check your prediction.


<details>
  <summary>Question: Do you understand why this rule failed?</summary>
  Answer: This rule is wrong. The `--optimistic_loop` flag required `n` to fit the number of times the loop is  unrolled (i.e. `require(!(i < n))`). In our case, since we didn't set the `--loop_iter` its value is default (1), so the requirement force `n = 1`. The function then returns 1, while we demand it to be equal to `2*1`.
</details>

</br>

- [ ] If we were to add `--loop_iter` flag with a larger number of loop unrolling what would've happen? Try running the last 2 runs (with the `--optimistic_loop`) using `--loop_iter` with values 3, 5 ,10.

<details>
  <summary>Question: Do you understand the results?</summary>
  Answer: the correct rule passed no matter the number of loop unrolling. That is because the loop always returns `n`, regardless of the actual `n` value. The `--optimistic_loop` is the only flag needed to make it pass, essentially saying to the Prover "just make sure that the loop will not iterate more than it should". </br>
  The wrong rule failed no matter what because once we established that the loop does not over iterate the rule is wrong regardless of the number of loops.
</details>

</br>

- [ ] Now say that we were to remove the `--optimistic_loop` and keep the 3, 5, 10 `--loop_iter`, what will be the results? Try it.

<details>
  <summary>Question: Do you understand why both rules failed?</summary>
  Answer: It doesn't matter how many times we unroll the loops, because the number of iteration is dependent on a parametric input, the Prover will always be able to assume the number of `--loop_iter` + 1 and return a violation.
</details>

</br>

Now we move to the constant iteration loop and do the entire procedure all over again. The rules failed when ran with neither `--optimistic_loop` nor `--loop_iter`.

- [ ] If we were to add `--loop_iter` flag to `const_loop_correct`, can you predict what the results would be?
Change the script and run it with value 3, 5, 10 for the `loop_iter` to check your prediction.

<details>
  <summary>Question: Do you understand why both rule failed/passed with each value of `loop_iter`?</summary>
  Answer: The rule is basically correct, however with any number of loop unrolling that is smaller than 5 (the loop condition) the loop fails since it considers the pessimistic case where we unrolled the loop `i < 5` times, and so there can be a violation in later iteration that we did not reach. </br>
  In any value of `loop_iter` that is greater or equal to 5, the pessimistic mode is negated because `i` reaches a value greater or equal to 5, which satisfy the loop condition, and doesn't leave any unchecked iterations.
</details>

</br>

- [ ] If we were to add `--loop_iter` flag to `const_loop_wrong`, can you predict what the results would be?
Change the script and run it with value 3, 5, 10 for the `loop_iter` to check your prediction.

<details>
  <summary>Question: Do you understand why both rule failed for all values of `loop_iter`?</summary>
  Answer: The rule is basically wrong. As in the previous run, for every value of `loop_iter` that is less than 5 we get the violation of the pessimistic mode, and for every value that is greater or equal to 5, we get a violation of the rule itself - the returned value is not equal the the stated value in the asset.
</details>

</br>

- [ ] If we were to add `--optimistic_loop` flag what would've happen? Try running the last 2 runs (with the `--loop_iter` 3, 5 ,10).

<details>
  <summary>Question: Do you understand the results?</summary>
  Answer: the correct rule passed no matter the number of loop unrolling. That is because the loop always returns `n` - the number of iterations the loop has done.
  When the number of loop unrolling was less than 5 we got a vacuous rule since the optimistic mode demanded `require (!(i < 5))` which is always false, i.e. we never reached the `assert`. For `loop_iter` greater or equal to 5 the rule passed correctly. </br>
  The wrong rule failed on every `loop_iter` value except for 3. For values less than 5 we failed because the returned value was other than 3 (we ran `loop_iter 1` when we didn't specify `loop_iter`), and on values greater or equal to 5 we failed because the loop will always return 5. However for `loop_iter 3` we've found a dangerous sweet spot where the the optimistic mode doesn't worn us that we never unrolled the loop enough to meet the condition, yet we unrolled it exactly the number of times needed to get our wrong rule right!
</details>

</br>

- [ ] Try running the previous runs again, this time with an `assert false` at the end of each rule. 

- [ ] Now remove the `assert false`, `--loop_iter` and keep the `--optimistic_loop`, what will be the results? Try it.

<details>
  <summary>Question: Do you understand the rules?</summary>
  Answer: In both rules for `loop_iter` with value less than 5 we failed on pessimistic mode (unwinding condition in a loop). For `loop_iter` greater or equal to 5 we fail on the wrong rule since the loop always return 5 but we demanded the return value to be 3, and on the correct rule we pass for the exact same reason - the loop always returns 5 and that is exactly what we demanded.
</details>

</br>

---

## Aftermath

<br/>

That whole segment may have been confusing, so we suggest that you go over it again if it wasn't completely clear.
The idea of this was to show that loop handling is a delicate subject with the Certora Prover, and it has to be treated with extreme delicacy.

There are 2 things to keep in mind when playing with the flags:

1. when tweaking a flag on it applies for the whole contract, meaning that if we have a constant loop of size 2 and a dynamic loop, setting the `--loop_iter` to 2 will make the dynamic loop to get verified with the same number of loop unrolling. This can impose a problem when multiple loop are to be run for the same rule verification.

2. usually cannot just raise the `--loop_iter` as much as we'd like, even if we have a hard limit on the loop (like the constant loop). Unrolling adds complexity which will rise the runtime of your specification.

Be clever with the use of loops flags.
On a parametric loop, it is often enough to check a small number of iterations to verify the entire rule (or at least give a very good coverage). 