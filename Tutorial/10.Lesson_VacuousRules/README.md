# Vacuous Rules and Invariants

There is a type of rule/property that doesn't check anything and will always pass regardless of input values. We call these rules [vacuous](https://en.wikipedia.org/wiki/Vacuous_truth).

Vacuous rules are extremely dangerous since they create false confidence in the properties of the system, which can lead to a premature deployment of a set of contracts.
Vacuous rules are way more common than you might think. When writing complex rules and invariants, it is easy to lose track and require too many assumptions. Sometimes these requirements may eliminate every possible route so that the assertion will never be reached (the ultimate under-approximation). Tautology is another case of vacuous assertions.

We will go through a few methods that should be applied after verifying a rule/invariant to check if it is vacuous.

</br>

---

## Catching Vacuity Caused By Under-Approximation

---
## MethodsVacuityCheck Rule

</br>

The first rule that a rule writer should write before starting implementing properties is the `MethodsVacuityCheck` Rule. It looks like this:

```
rule MethodsVacuityCheck(method f) {
	env e; calldataarg args;
	f(e, args);
	assert false, "this method should have a non reverting path";
}
```

This rule calls every function in the contract and then `assert false`. It tries to capture vacuous **functions** in the contract.
The results we get should always be thumbs down since assert false will always throw a violation. However, if the contract itself has a function that reverts every time it's being called regardless of input, then the function is vacuous, alerting the developers (because it does nothing).

- [ ] Create a `.spec` file named "Sanity" and write the `MethodsVacuityCheck` rule. Run a verification against [ERC20Fixed.sol](ERC20/ERC20Fixed.sol) and [ERC20Bug1.sol](ERC20/ERC20Bug1.sol).

- [ ] Find the bug in `ERC20Bug1`, fix it, and rerun the verification to verify that you get an all thumbs down result.

> :bulb: Remember, when running a sanity rule, we want to see an all-failing results report.

</br>

---

## Adding `assert false` and `--rule_sanity` Flag

</br>

Once a rule/invariant we've written has passed, we should use either of the following two methods to check it's not vacuous. 

### Adding `assert false`

</br>

By adding an `assert false` to the last line of a rule and expecting it to fail, we're asking the question - "Is there a path (set of values) that reached our original last assert and passed it?".
When we fail the newly added assert, the answer to our question is "Yes - there is a set of values that reached and passed our last original assert". If all paths were to revert before reaching our `assert false`, this assert will have never been checked in the first place.

### `--rule_sanity` Flag

When running a verification with the `--rule_sanity` flag, the tool runs the rule/invariant twice - once as written, and again changing the original asserts to requires and adding an `assert false` at the end. It combines the results and indicates whether the `assert false` did not fail, meaning the rule/invariant is empty.

You can read more about the `--rule_sanity` flag in the documentation [Link](https://certora.atlassian.net/wiki/spaces/CPD/pages/7340043/Certora+Prover+CLI+Options#--rule_sanity[inlineExtension])

> :warning: The indication given for `--rule_sanity` at the moment is :warning: over a red background. A better presentation should be integrated soon.

</br>

Both vacuity checking methods are equally as good. Since the `--rule_sanity` flag is still evolving, there are slight advantages and disadvantages to each of them:

- Manual addition of an `assert false` require tweaking the spec file and firing two runs but shows a counter example. Since only values that pass our original asserts should get to the assert false, we can see and investigate an example of a valid set of variables.

- `--rule_sanity` mashes all the data together and saves the need to alter the code and run the tool multiple times. However, as this is still an evolving feature, its indicator can still be confusing, and it does not show a counter example. 

Soon enough, `--rule_sanity` will implement the missing features and be the method of choice, so stay tuned to new feature releases and fixes.

</br> 

--- 

## Catching Vacuity Caused by Tautology

</br>

Adding an `assert false` as the last line of invariants is syntactically impossible in CVL.
What we can do is generate a rule that has exactly 1 line in it - `assert exp`:

``` CVL
invariant vacuousInvariant(uint x, address y)
    exp

rule checkVacuousInvariant(uint x, address y){
    assert exp
}
```

Since in `checkVacuousInvariants` we make no assumptions prior to the assert, the Prover may consider any combination of values to the set of variables, without restrictions. This rule should fail unless the expression is a tautology. We should suspect `checkVacuousInvariants` if it does pass.

We can do the same for some rules we write. We can check whether the expression is a tautology by taking the asserted expression at the end and shoving it into a singled-line rule.
Note that it's not always easy to do, for example, for rules that compare the state before and after a function call.

> :information_source: Soon this method of checking vacuity will be implemented as part of the `--rule_sanity` flag.

</br>

---

## Aftermath and an Additional Method - Adding Bugs to the Contract

</br>

It is important to understand that there are many cases where your rule can be vacuous, yet neither of the methods above will catch the mistake.
It is crucial to be suspicious and alert even when all methods above indicate that the rule isn't vacuous.

To further check your coverage, you can apply the following method mentioned in [07.Lesson_InductiveReasoning](../07.Lesson_InductiveReasoning).
Adding bugs to the code that your rule should catch is probably the best way to check your rule. This method will not necessarily indicate that the rule is vacuous, but it will suggest that the property does not cover as much ground as you would've liked.
This method will catch vacuity caused by both tautology and under-approximation.

</br>

---

## Exercise

</br>

- [ ] Read the entire `"Simple Map"` example from the documentation. - [Link](https://docs.certora.com/en/latest/docs/user-guide/map/simple.html). Focus in particular on the option of calling a function `@withrevert` and the corresponding storage data of `lastReverted`.

- [ ] Read the common pitfalls article on vacuity [Link](https://docs.certora.com/en/latest/docs/confluence/pitfalls.html?highlight=lastreverted#lastreverted-updates).

- [ ] Go over the rules and invariants in [ERCVacuity](ERC20/ERCVacuity.spec). Use the methods you've just learned to determine if they are vacuous rules.
 
- [ ] Go back to the `.spec` files that you've written for the `Spartan Protocol` and `Popsicle Finance`, and look at them with a new point of view. Try to apply the methods we've learned in this lesson to check whether you've written any vacuous rules and invariants.

- [ ] If you did write vacuous rules, try to rethink if the rules make sense in the first place. If they do, fix them.

</br>

---

## Loops

</br>

- [ ] Continue to the next lesson: [Loops](../11.Lesson_Loops) to learn about the complexity of handling loops and ways to approach it.

</br>

---

### “If people never did silly things, nothing intelligent would ever get done.” — Ludwig Wittgenstein

---
