# Inductive Reasoning

In this tutorial, you will practice understanding counter-examples produced by Certora Prover on induction reasoning. 
As discussed, the tool assumes all possible input values and states as valid starting states. Some of them are infeasible, which means that no set of operations, starting from the constructor, will lead to those states.

</br>

---

## Simple Example - Ball Game

</br> 

Start with [Ball Game](BallGame/BallGame.sol), implementing a ball game with four players:

- Player 1 passes the ball to Player 2.
- Player 2 passes back to Player 1.
- Player 3 and 4 pass to each other.

The ball starts at Player 1. Let's prove that the ball can never reach Player 4.

- [ ] Run the `BallGame.spec` file supplied in the directory and investigate the counter-example.
Do you understand what fails?

The initial state in the counter example is 3.
The Certora Prover was instructed to verify that the ball can never be at the hands of player 4 in the form of invariant so it:

1. Verified that the expression is true after the constructor.

2. Restricted the initial states to be anything other than player 4 with a precondition.

3. Invoked any function in the contract.

4. Checked if the condition still holds after applying step 3 on the state defined in step 2.

The initial state "ball at the hands of player 3" is a possible state by the pre-condition.

- [ ] Fix the invariant to avoid superfluous initial states.

We learned here that in order to prove the required property we needed to prove a stronger invariant.

- [ ] Try writing the invariant as a parametric rule. Make it pass.

- [ ] Change the initial state in the solidity contract from `ballAt = 1` to `ballAt = 3` and rerun the same full spec file with the invariant and rule that passed.

Did you expect the new results?
Do you understand why the invariant fails and the rule passes?

This shows the difference between invariant and rule:  

While an invariant checks the expression in the classic two induction steps:

1. ***Base Step***: Verifying the expression on the constructor.

2. ***Inductive Step***:
</br>
    2.1 Assuming the expression holds, (in practice restricting the set of possible values to take into account by the solver).

    2.2 Taking a step by applying a function and then verifying the expression on the new state by assertion.

A rule starts straight from the inductive step (2.), assuming the expression is true (2.1), then taking a step and asserting the new state (2.2).

</br>

---

## Advanced Example 

</br>

For a more realistic example, [Manager](Manager/Manager.sol) implements transferring the management role of a fund. It is a requirement that an address can manage only one fund. Let's try to prove this property.

[Manager.spec](Manager/Manager.spec) contains a typical parametric rule.

- [ ] Run the `Manager.spec` file supplied in the directory and investigate the counter-example. 
Do you understand what fails?

- [ ] Understand the counter-examples and try thinking which additional properties are related and need to be proven together.

- [ ] Fix the rule.

- [ ] Check your rule as sometimes the rule is too strict and overly limits the possible initial states or executions.

    - [ ] To check your rule, intentionally insert bugs into the contract. Insert bugs that should be detected by the rule (fail verification).

    - [ ] Rerun the Certora Prover to get a counter example that fits your expectation.

- Run the rule on the pre-prepared buggy versions of the code:
[ManagerBug1](Manager/ManagerBug1.sol) and [ManagerBug2](Manager/ManagerBug2.sol)
    
Did your rule find violations?

- [ ] Try running the version of the rule as an invariant.

Is this property an invariant of the system?

- [ ] Now, after trying to write the rule, have a look at the [Partial Solution](Manager/ManagerPartialSolution.spec). This is an almost correct implementation of the rule.
    
    - [ ] Run the partial solution on the two buggy implementations of manager. Why doesn't it fail on both of them as expected?

    - [ ] The solution pass on [ManagerBug1](Manager/ManagerBug1.sol) because the condition is too strict. Can you find the problem and fix it?

### Explanation - Under/Over-Approximation

</br>

As we've seen before, the Certora Prover is over-approximating states by design to avoid false positives. This design creates false negatives (violations) that can be eliminated by proving the set of reachable states.

In the case of the [Manager Partial Solution](Manager/ManagerPartialSolution.spec), we've created an under-approximation of the initial state via the pre-condition, i.e. we demanded (assumed) too strict a condition that made the tool disconsider some feasible states. We see that this under-approximation created a false positive (verification passed) that could've made us believe that the (buggy) implementation is flawless in terms of having a unique manager.

This is a classic example of incorrect usage of precondition in rules.

- [ ] Once you know how to fix the expression, try to run 2 verifications on [ManagerBug1](Manager/ManagerBug1.sol):

    - [ ] Correct the post-condition while leaving the too-strict pre-condition.

    - [ ] Correct the pre-condition while leaving the "too-strict" post-condition.

Notice which of them pass the verification falsely and which caught the bug.
Do you understand why these are the results?

Hint - the difference is the sample space that the pre-condition creates for the assert.

Upload your solutions for review.