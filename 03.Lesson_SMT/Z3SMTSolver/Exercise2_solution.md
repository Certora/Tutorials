# Exercise 2 solution in z3 code

```z3
(declare-const p Bool)
(declare-const q Bool)
(define-fun conjecture () Bool (= (= (and p q) p) (=> p q)))
(assert (= (not conjecture) true)) ; there exists case where negation of conjecture is true
(check-sat) ; unsatisfied, meaning the negation is always false
```

assert satisfied so the two equations are equivalent
