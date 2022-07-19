Invariants
==========

Invariants are an important concept for writing and reasoning about code.
This lesson describes invariants and explains how they can be checked and used
by the Certora Prover.

</br>

---

A motivating example
--------------------

</br>

Consider the [Bank contract from lesson 1](Bank/BankFixed.sol). An important property for any bank to have is that if you are owed some funds, you can withdraw them.
Let's take a look at the Bank's `withdraw` method and see if it has this
property:

```soldity
function withdraw() public returns (bool success)  {
    uint256 amount = getFunds(msg.sender);
    funds[msg.sender] = 0;
    success = msg.sender.send(amount);
    require(success);
    totalFunds = totalFunds.safeSub(amount);
}
```

It seems like this method does what we want.  When we call `withdraw`, if we
are owed `x` ETH, then `getFunds(msg.sender)` returns `x` (line 39), and then
the contract sends `x` ETH to us (line 41).  We get our funds.

What might go wrong?  Well, if the bank doesn't have enough ETH to send us, the
call to `msg.sender.send` on line 41 will fail, causing the transaction to
revert.  We would not be able to withdraw our funds!

</br>

---

Is the Bank actually broken?
----------------------------

</br>

If we run the prover, we see that it would give us a counterexample describing
exactly this situation[^withrevertnote]:

```cvl
rule can_withdraw() {
    env e;

    uint256 balance_before = getEthBalance(e.msg.sender);
    uint256 reserves       = getEthBalance(currentContract);
    uint256 funds_before   = getFunds(e.msg.sender);

    withdraw@withrevert(e);

    uint256 balance_after  = getEthBalance(e.msg.sender);
    assert balance_after == balance_before + funds_before;
}
```

[^withrevertnote]: The `@withrevert` annotation on the call to `withdraw` tells
                   the prover to consider cases when `withdraw` reverts;
                   the default behavior is to ignore counterexamples that cause
                   reverts.

The prover produces a counterexample with `funds_before = 5` but
`getEthBalance(currentContract) = 3`; the call to `send` reverts, and the
`balance_after` is the same as `balance_before`.

- [ ] Run the rule `can_withdraw()` in [invariant.spec](Bank/invariant.spec) and get the violation for yourself.

> :warning: Remember that the SMT may retrieve different counter example to the same case.

Despite this counterexample, the withdraw method is actually correct. It is
true that _if_ the bank's ETH balance is too low then `withdraw()` will revert
inappropriately, but if the rest of the code is correct, then the bank's ETH
balance should _never_ get too low.

</br>

---

Enter Invariants
----------

</br>

The property that the balance should never get too low is an example of an
**invariant**.

> :warning: An [invariant](https://en.wikipedia.org/wiki/Class_invariant) is a fact about the state of the system that should always[^between_transactions] be true.

[^between_transactions]: Invariants may temporarily become false within a
  transaction, but they should be reestablished by the end of a transaction.
  The violations should be invisible to the outside world.

Invariants only describe the state of the system at a single point in time,
they do not describe what happens as the state changes or how the system got into a particular state. If you can determine whether a statement is true by just looking at the fields and ether balances of one or more contracts, and you expect the statement to always be true, then the statement is an invariant.

"The bank's ETH balance should never be lower than any user's funds" meets these criteria:
 - you could check whether it's true by looking at `funds[u]` for all `u` and comparing them to the ETH balance of the `Bank`

 - we expect the Bank to always keep enough ETH to pay back the users.

</br>

<details>
  <summary>Question: is "the user's funds are greater than 0" an invariant?</summary>
  Answer: No. You can check whether it's true by examining `funds[u]` for all `u`, but users are allowed to have balances of 0.
</details>

<details>
  <summary>Question: is "`deposit` increases the bank's ETH balance" an invariant?</summary>
  Answer: No. You can only check this by comparing the ETH balance before and after the deposit.
</details>

<details>
  <summary>Question: is "if a user's funds are greater than 0, then the user must have called `deposit` in the past" an invariant?</summary>
  Answer: No. There is no way to tell if the user called deposit by looking at the fields of the contract. You could make this into an invariant by recording
  calls to `deposit` in a field of the contract.
</details>

<details>
  <summary>Question: is "1 > 0" an invariant?</summary>
  Answer: Technically yes, although it's not very useful!  You don't need anything besides the state of the system to check whether it's true, and you expect it
  to always be true.
</details>

</br>

---

Using invariants to show solvency of the bank
----------------------------------------------

</br>

Before we jump into verifying concrete properties using invariants, let's go over the syntax:

```CVL
invariant inv_name(argType arg1, argType arg2, ...)
    exp
```

As you might noticed, the syntax is fairly simple:

1. A declaration of an invariant `invariant` following by the invariant name `inv_name`.
2. A list of argument - a list of variables the invariant needs to generate for its scope.
3. An expression that must hold at any point in time[^between_transactions].

> :warning: Note that the invariant is not wrapped with curly brackets.

Now let's move on to a concrete example of an invariant.
We'd like to show that the bank always holds enough funds to pay up its customers; so we may come up with the property - "the `totalFunds` in the bank is always greater or equal to a single user's balance". If we were to verify this property, an arbitrary user that would like to withdraw its funds will surely be able to do it.

The invariant would look like that:

```CVL
invariant totalFunds_GE_single_user_funds()
    forall address user. getTotalFunds() >= getFunds(user)
```

> :bulb: This invariant contains the quantifier `forall`. Quantifiers are supported in CVL, however they add a fair amount of complexity on the SMT, which usually make the rule timing out[^Timeout].

[^Timeout]: Timeout is an intentional stop of the run (hard stop) after a predefined amount of time due to failure to produce a result. We define such a hard stop due to [the halting problem](https://en.wikipedia.org/wiki/Halting_problem).

- [ ] Run the invariant for yourself to see the results.

However, although the invariant does verify that each user's balance must be less than the `totalFunds`, it does not promise that the `totalFunds` covers the sum of all users' balances. In other words the case where there are 2 users in the system: `funds[userA] = 8`, `funds[userA] = 6` and `totalFunds = 10` is valid. This case is clearly not what we meant. Each user can withdraw its balance, but once one has withdraw, there isn't enough money in the bank to pay the other user its deserved funds.

Rethinking, we may come up with a second invariant that should always hold - "The sum over all users' balances should be less then or equal to the total funds in the system". If funds are only being transferred within the system, then equality should hold, but for our purpose we don't mind that the bank will hold extra ETH transferred from external source to make sure that the bank is solvent.

To track the sum of all users' balances we'll need to use a new concept - a ghost.
We'll learn about ghosts more profoundly in a later lesson [13.Lesson_Ghost](../../13.Lesson_Ghost), so for now follow the comments on the `.spec` file to understand what it does.

Our new invariant would look like this:

```CVL
ghost sum_of_all_funds() returns uint256{
    init_state axiom sum_of_all_funds() == 0;
}

hook Sstore funds[KEY address user] uint256 new_balance(uint256 old_balance) STORAGE {
  havoc sum_of_all_funds assuming sum_of_all_funds@new() == sum_of_all_funds@old() + new_balance - old_balance;
}

invariant totalFunds_GE_to_sum_of_all_funds()
    getTotalFunds() >= sum_of_all_funds()
```

This time we make sure that there is enough money in the bank to pay all users in case everybody wants to withdraw their funds.

> :bulb: Note that this invariant covers the previous one - if `totalFunds` is greater or equal to the sum of all users' balances, it's in particular greater or equal to any specific user's balance.

- [ ] Run the invariant `totalFunds_GE_to_sum_of_all_funds` to see the results.

- [ ] Duplicate the invariant and change the inequality to a strict equality, i.e. `getTotalFunds() == sum_of_all_funds()`. </br>
Run the new invariant to see the results.

</br>

---

How the Prover checks invariants
--------------------------------

</br>

And now, it's time to reveal the trick behind the magic - **how invariants are proven?**

Invariants are being proved by following the classic two induction steps:

1. ***Base Step***: Verifying the expression on the constructor.

2. ***Inductive Step***:
</br>
    2.1 Assuming the expression holds, (in practice restricting the set of possible values to take into account by the solver).

    2.2 Taking a step by applying a function and then verifying the expression on the new state by assertion.

In practice, the Certora Prover translate the invariant into parametric rules that follow this particular structure:

The following generic invariant:

```CVL
invariant generic(uint256 a, address x, ...)
    exp(a, x, ...)
```

is being translated into the following parametric rules:

```CVL
rule translation_of_generic_invariant_init(method f, env e, uint256 a, address x, ...){
    call constructor();
    assert exp(a, x, ...);
}

rule translation_of_generic_invariant_body(method f, env e, uint256 a, address x, ...){
    require exp(a, x, ...);
    f(e, args);
    assert exp(a, x, ...);
}
```

Writing an invariant lets us express a complete property that covers the system from the very beginning - the constructor, in a very elegant and concise manner.

In the next lesson we will learn about ***preserved blocks*** which adds a block of code right at the beginning of the second parametric rule (the "body").

<details>
  <summary>Question: Why both forms: <code>>=</code> and <code>==</code> in <code>totalFunds_GE_to_sum_of_all_funds</code> passed?</summary>
  Answer: The prover starts with an arbitrary initial state, and take a step from there with one of the functions specified in the contract. </br>
  Transferring ETH to/from outside the contract is possible in reality, but isn't considered by the Prover since no such function is implemented in the verification context. In other words, the prover tries to abuse the functions it has in hand, and cannot predict malicious actions of functions that aren't explicitly specified to it (re-entrancy for example is tough to predict).
</details>