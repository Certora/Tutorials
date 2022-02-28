# Exercise 1 solution in z3 code

```z3
(declare-const g Int)
(declare-const y Int)
(declare-const r Int)
(assert (= (+ g g) 10))
(assert (= (+ (* g y) y) 12))
(assert (= (- (* g y) (* r g)) g))
(check-sat)
(get-model)
```

The red triangle (constant r above) is equal to 1
