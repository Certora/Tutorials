# Handling Loops

Loops knowingly has 2 problems that impose difficulty on computation and needs to be taken into consideration by programmers:

1. [The halting problem](https://en.wikipedia.org/wiki/Halting_problem).

2. It introduces a considerable increase in the amount of commands executed in a program.

Solidity (and ethereum in general) covers the halting problem quite well by introducing gas to the using process. The raise in complexity, however, can make life very difficult on the SMTs, which necessitates special handling. The way that was chosen to handle this problem is by making an approximation - [Loops Unrolling](https://en.wikipedia.org/wiki/Loop_unrolling).

- [x] Read the documentation on [loops unrolling](https://docs.certora.com/en/latest/docs/ref-manual/approx/loops.html) to learn how to approach verifications of programs that includes loops. Make sure to read the documentation on [--loop_iter](https://docs.certora.com/en/latest/docs/ref-manual/cli/options.html#loop-iter) and [--optimistic_loop](https://docs.certora.com/en/latest/docs/ref-manual/cli/options.html#optimistic-loop) as well.

As we mentioned before, the Certora Prover does not run in the traditional sense like most programming languages; instead, it takes the assignments, boolean expressions and mathematical computations performed in a program (contract) and generates a set of symbolic equations out of them. The number of equations generated when a loop is involved is raising quickly which can impose quite a lot of difficulty on the Prover if the computations are complex.

</br>

---

## Exercise

</br>

- [x] Go over the interactive example in [Loops Example](LoopsExample) to see how the flags `--optimistic_loop` and `--loop_iter` work on simple cases and learn the danger of wrong flagging.

</br>

- [x] Follow the instructions on [BankLoops](BankLoops) to exercise loop handling with correct use of `--optimistic_loop` and `--loop_iter`.


</br>

---

## Multi Contract Verification

</br>

- [ ] Continue to the next lesson: [Multi Contract](../12.Lesson_MultiContract) to learn how to verify contracts that interact with other contracts.

</br>

---

### “We are trying to prove ourselves wrong as quickly as possible, because only in that way can we find progress.” ― Richard P. Feynman

---
