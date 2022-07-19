# Bank With Loops

In this directory you will find the fixed bank implementation from lesson 1, with 2 additional functions - `multiTransfer` and `multiTransferWithBug`, and a `.spec` file with a couple of rules.

> :warning: We still haven't encountered ghosts, but don't be intimidated by them, ghost are your friends! We will learn about ghost in [Lesson 13](../../13.Lesson_Ghost). In the meanwhile read the comments on them.

- [ ] Run the rules with no loops-handling flags and see the results. Are all failures occur because on functions that should fail the asserts?

- [ ] add the appropriate flags to pass the rules that should pass un-vacuously and get a proper counter example for scenarios that should fail for a logical reason. Use an `assert false` at the end of the rule to double check that your rule doesn't pass vacuously.

<details>
<summary>Hint:</summary>
Try inserting flags one by one. Remember the `multiTransferWithBug` <b>must</b> to fail because it does not preserve the total funds for any arbitrary number of iterations.
</details>