# Z3 logical prover
### Z3 is a state-of-the-art theorem prover from Microsoft Research. It can be used to check the satisfiability of logical formulas over one or more theories.

---

## Basic Commands
1. The Z3 input format extends the one defined by the [SMT-LIB 2.0 standard](https://web.archive.org/web/20210125011020/http://www.smtlib.org/).
2. Each command should be enclosed in round parentheses ( …. ) .
3. Some basic useful commands:
	1. `( help )` command displays a list of all available commands.
	2. `( echo “message” )` displays a message.
		1. Example: `( echo “Z3 Prover is cool” )`.
	3. `( declare-const var type)` declares a constant of a given type.
		1.  Example: `( declare-const num Int )`.
	4. `( declare-fun f (input_para1 input_para2 …) output_para)` declares a function.
		1.  Example: `( declare-fun f  (Int Bool) Int )`.
	5. `( assert (logical_operator LHS RHS) )` adds a formula into the Z3 internal stack, where LHS and RHS stand for Left and Right Hand Side of the operator.
		2. Example 1: `(assert (> a 10))`.
		3. Example 2: `(assert (< (f a true) 100))`.
	6. `( check-sat )` execute all assertion checks up to this line.
		1. Outputs “sat” satisfied, and “unsat” if unsatisfied (see point No. 4). Outputs “unknown” if it can’t determine.
	7. `( get-model )` gives an example (interpretation) that makes all formulas true.
		1. Output Example 1: `(define-fun a () Int  11)` —> a = 11.
		2. Output Example 2: `(define-fun f ((x!0 Int) (x!1 Bool)) Int  0)` —> f returns 0 for any x0 int and x1 bool.
4. The set of formulas in a stack is satisfiable if there is an interpretation that makes all asserted formulas true. If such an interpretation exists, we say it is a model for the asserted formulas. Meaning, if every assertion before (check-sat) can be satisfied with a single set of values it is satisfiable. It is “unsat” if even a single assertion can’t be satisfied.

---

## Scopes
1. Scopes are useful when we want to explore several similar problems that share several definitions and assertions.
	1. It dictates a workflow where the commands relevant to all scopes are declared in the beginning, pushed (i.e., saved to the scope).
	2. `( push )` creates a new scope by saving the current stack size.
	3. `( pop )` removes any assertion or declaration performed between it and the matching push.
        1. Each push-pop pair is equivalent to open-close pair of a scope.


---

## Configuration
1. Some commands are used to configure behavior of the interpreter.
	1. `( set-option :option bool_value )` sets the Z3 behavior. Some options can only be set prior to any declaration or assertion.
		1.  Example 1 : `( set-option :print-success true )`
		2.  Example 2 : `( set-option :proof true )`
	2.  `( reset )` erase all assertions and declarations.
		1.  After the reset command, all configuration options can be set.

---

## Additional Commands
1. `( display t)` applies the Z3 pretty printer to the given expression (displays it nicely).
	1. Example: `(display (+ x 2 x 1))`
2. `( simplify t )` displays a possibly simpler expression equivalent to t.
	1. This command accepts many different options, to see the options run `( help simplify )`.
	2. Example: `( simplify (+ x 2 x 1) )` will output ( + 3 (* 2 x) ),
3. `( define-sort abbreviation_symbol ( symbol sort ) )` defines a new sort symbol that is an abbreviation for a sort expression.
	1.  Example : `( define-sort I () Int) (declare-const a I)`

---

## Propositional Logic
1. In Z3 every Boolean expression is defined as Bool. It supports the following operators:
	1. And, or, xor, not, => (implication), ite (if-then-else), = (Bi-implications).
	2. Example:
	``` 
	(declare-const q Bool)
	(declare-const q Bool)
	(declare-const r Bool)
	(define-fun conjecture () Bool
    		 (=> (and (=> p q) (=> q r))
        		 (=> p r)))
	(assert (not conjecture))
	(check-sat)
	```

---

## Satisfiability and Validity
1. A formula F is ***valid*** if F always evaluates to true for any assignment (appropriate to its type).
2. A formula F is ***satisfiable*** if there is some assignment (appropriate to its type) under which F evaluates to true.
3. ***Validity*** is about finding a proof of a statement;
	***Satisfiability*** is about finding a solution to a set of constraints.
4. If **F** is always true, then **not F** is always *false*.
	Then, **not F** will not have any satisfying assignment; that is, **not F** is *unsatisfiable*.
	That is, **F** is *valid* precisely when **not F** is not satisfiable (unsatisfiable), i.e., not F unsatisfiable => F valid.
	2. F satisfiable <=> not F invalid (not valid).

5. To determine whether a formula F is valid, we ask Z3 whether not F is satisfiable. Z3 finds satisfying assignments or report that there are none.
	1. A good example is in exercise 2 at the bottom of the file - we define a conjecture and ask Z3 to find a satisfying value to the **Not F** if it can’t find such value to satisfy it, that means that it is valid (by 4.1)
---
## Uninterpreted functions and constants
1. In Z3, constants are just functions that take no arguments. So everything is really just a function.
2. Functions in classical first-order logic have no side-effects (exceptions, no return) and are **total**. That is, they are defined on all input values [[1](https://mathworld.wolfram.com/TotalFunction.html)]. This includes arithmetic functions.
3. In pure first-order logic, function and constant are *uninterpreted* or *free*, meaning that no prior definition/interpretation is attached to the function. The SMT allows itself to define the function as it wishes within the constraints.
	1. For example, the arithmetic function “+” is not pure because it is pre-defined for a specific interpretation (adding two numbers).
4. `( define-sort symbol )` defines an uninterpreted data type. 
---
## Arithmetics
1. `( declare-const var_name Int )`, `( declare-const var_name Real )` defines mathematical Integer and Real constants.
	1. Real constants should contain a decimal point.
	2. Z3 will not automatically convert integers into reals and vice-versa. The function **to_real** can be used for the conversion.
2. After constants are declared, an assertion containing them can be made using assert.smt formulas.
	1. The formulas contain arithmetic operators such as +, -, <, and so on.
3. The formula (* t s), where t and s are not numbers, is nonlinear.
	1. Nonlinear real arithmetic is very expensive, and the Z3 is not built for it. When checked `( check-sat )`, it may return “unknown” or loop.
	2. Nonlinear integer arithmetic is “undecidable” - there is no procedure that, for every input, can determine a “sat” or “unsat” answer.
		1. Note that it is impossible to develop a procedure that will find an answer all the time, but an answer can still be found sometimes.
4. Division, integer division, modulo, and remainder operator are represented as: **/**, **div**, **mod**, and **rem** respectively.
	1. Internally, these operators are all mapped to multiplication.
5. Division by zero is allowed, but the result is not specified (i.e., there is no arithmetic result to the operation). In Z3, all functions are total, although there might not be a specified result in some cases.
	1.   The following code describes the tricky behavior of division by 0:
	
	```
	(declare-const a Real)
	; The following formula is satisfiable since division by 		zero is not specified.
	(assert (= (/ a 0.0) 10.0)) 
	(check-sat)
	(get-model)

	; Although division by zero is not specified, division is still a function.
	; So, (/ a 0.0) cannot evaluated to 10.0 and 2.0.
	(assert (= (/ a 0.0) 2.0)) 
	(check-sat)
	```
	Even though a result might not be specified, the same operation (dividing a by 0) cannot return two different answers.
	2. This behavior can be bypassed using the ite (if-then-else) operator to specify the behavior of division by 0 explicitly. A convenient manner of doing so is by defining a div_zero function.
