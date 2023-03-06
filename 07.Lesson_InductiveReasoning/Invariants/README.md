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

Consider the [EnglishAuction](EnglishAuction/EnglishAuction.sol). There are the following fields of the contract 

```soldity
    address public highestBidder; //The address that bided the highest bid
    uint public highestBid; //The amount of the highest bid
    mapping(address => uint) public bids; //The amount each address has bided for
}
```

A rather straightforward expected property from this system:

```bids[highestBidder] == highestBid``` 

</br>

---

Is the Action code broken?
----------------------------

</br>

If we run the prover, we see that it would give us a counterexample for highestBidVSBids. This invariant fails to be proven after the constructor.  However the code is correct, the constructor assign to highestBid the minimum price for the auction, every bid has to increase the highestBid.

Try to fix the invariant.



What about the bids of other addresses than the highestBidder?

look at invariant `integrityOfHighestBid` 
```
 bids(any) <= highestBid()  
```
---

Recap on Invariants
----------

</br>

The above properties are an example of an
**invariant**.

> :warning: An [invariant](https://en.wikipedia.org/wiki/Class_invariant) is a fact about the state of the system that should always[^between_transactions] be true.

[^between_transactions]: Invariants may temporarily become false within a
  transaction, but they should be reestablished by the end of a transaction.
  The violations should be invisible to the outside world.

Invariants only describe the state of the system at a single point in time,
they do not describe what happens as the state changes or how the system got into a particular state. If you can determine whether a statement is true by just looking at the fields and ether balances of one or more contracts, and you expect the statement to always be true, then the statement is an invariant.


</br>

<details>
  <summary>Question: is "the highestBid greater than 0" an invariant ?</summary>
  Answer: It's an invariant as it is an expression of a state. However it is not correct - highestBid can be zero in the constructor.
</details>

<details>
  <summary>Question: is "`highestBid` increases at every bid" an invariant?</summary>
  Answer: No. You can only check this by comparing the highestBid before and after the bid. It's a rule.
</details>

<details>
  <summary>Question: is "if a user's bids are greater than 0, then the user must have called `bid` in the past" an invariant?</summary>
  Answer: No. There is no way to tell if the user called deposit by looking at the fields of the contract. You could make this into an invariant by recording
  calls to `deposit` in a field of the contract.
</details>

<details>
  <summary>Question: is integrityOfHighestBid an invariant?</summary>
  Answer: Yes, and it holds, but is it a strong one? It contains states that you would consider not correct, two users had the highestbid. 
</details>


<details>
  <summary>Question: is "1 > 0" an invariant?</summary>
  Answer: Yes but it's a tautology.
</details>

</br>



- [ ] Run the invariant to see the results.

- [ ] Can you think of more invariants that should holds, just write them done

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

In practice, the Certora Prover translates the invariant into parametric rules that follow this particular structure:

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

In the next lesson, we will learn about ***preserved **blocks*** which add a block of code right at the beginning of the second parametric rule (the "body").

