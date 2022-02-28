# Additional Exercise solutions in z3 code

## Problem 1, correct answer is D

```z3
(declare-const p Bool)
(declare-const q Bool)
(define-fun conjecture () Bool (=> p q))
(assert (= conjecture false))
(check-sat)
(get-model)
; answer a
(push)
(assert (and (not p) (not q)))
(check-sat)
(get-model)
(pop)
; answer b
(push)
(assert (and p q))
(check-sat)
(get-model)
(pop)
; answer c
(push)
(assert (and (not p) q))
(check-sat)
(get-model)
(pop)
```

## Problem 2, correct answer is C

```z3
(declare-const p Bool)
(declare-const q Bool)
(define-fun conjecture () Bool (=> (or p q) p))
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```

## Problem 3, correct answer is B

```z3
(declare-const p Bool)
(declare-const q Bool)
(define-fun conjecture () Bool (and (and p (or q (not p))) (not q)))
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```

## Problem 4, correct answer is A

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; ￢(￢p ⋁ ￢q ⋁ ￢r) = p ⋀ q ⋀ r
(define-fun conjecture () Bool (= (not (or (not p) (not q) (not r))) (and p q r)))
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```

## Problem 5, correct answer is C

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; ￢((￢p ⋁ q) ⋀ (p ⋁ ￢q))
(define-fun conjecture () Bool (not (and (or (not p) q) (or p (not q))))) 
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```

## Problem 6, correct answer is C

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; ￢((p ⋀ q) ⋁ (￢p ⋀ ￢q))
(define-fun conjecture () Bool (not (or (and p q) (and (not p) (not q)))))
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```

## Problem 7, correct answers are A B C D

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; M := p ⋁ ￢p
(define-fun conjecture () Bool (or p (not p))) 
; A) p ⋁ ￢p
(push)
(assert (=> (or p (not p)) conjecture))
(check-sat)
(pop)
; B) p ⋀ ￢p
(push)
(assert (=> (and p (not p)) conjecture))
(check-sat)
(pop)
; C) (p ⋀ ￢p) ⋁ ￢p
(push)
(assert (=> (or (and p (not p)) (not p)) conjecture))
(check-sat)
(pop)
; D) (￢p ⋁ p) ⋀ ￢p
(push)
(assert (=> (and (or (not p) p) (not p)) conjecture))
(check-sat)
(pop)
```

## Problem 8, correct answers are A B C D

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; M := p ⋁ ￢p
(define-fun conjecture () Bool (and p (not p))) 
; A) p ⋁ ￢p
(push)
(assert (=> (or p (not p)) conjecture))
(check-sat)
(pop)
; B) p ⋀ ￢p
(push)
(assert (=> (and p (not p)) conjecture))
(check-sat)
(pop)
; C) (p ⋀ ￢q) ⋁ ￢r
(push)
(assert (=> (or (and p (not q)) (not r)) conjecture))
(check-sat)
(pop)
; D) (￢p ⋁ p) ⋀ ￢p
(push)
(assert (=> (and (or (not p) p) (not p)) conjecture))
(check-sat)
(pop)
```

## Problem 9, correct answer is C

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; (p => (q => r)) => ((p => q) => r)
(define-fun conjecture () Bool (=> (=> p (=> q r)) (=> (=> p q) r)))
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```

## Problem 10, correct answer is A

```z3
(declare-const p Bool)
(declare-const q Bool)
(declare-const r Bool)
; ((p => q) => r) => (p => (q => r))
(define-fun conjecture () Bool (=> (=> (=> p q) r) (=> p (=> q r)) ))
(push)
; case exists where its false
(assert (= conjecture false))
(check-sat)
(pop)
(push)
; case exists where its true
(assert (= conjecture true))
(check-sat)
(pop)
```
