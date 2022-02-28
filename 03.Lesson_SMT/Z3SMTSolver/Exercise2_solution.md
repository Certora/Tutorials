# Exercise 2 solution in z3 code

```z3
(declare-const p Bool)
(declare-const q Bool)
(define-fun conjecture () Bool (= (= (and p q) p) (=> p q)))
(assert (= conjecture true))
(check-sat)
```

assert satisfied so the two equations are equivalent
