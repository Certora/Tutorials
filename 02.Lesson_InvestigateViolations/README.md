# Understanding Violations and Following Counter Examples

In this module we will get familiar with Certora Prover's counter examples for rules' violations.

In current directory there are 3 sub directories - [Borda Election](Borda), [Meeting Scheduler](MeetingScheduler), and [OpenZeppelin's ERC20](ERC20). 
Each sub directory contains a system interface, a spec file with pre-written rules, and a few solidity files that implement the interface.
Each implementation is a corrupted version of a real system, that contains bugs aimed to raise violations in the pre-written rules in the spec file.
In the sub directories you will also find a README file with hints and tips for each rule failure. If you get stuck try the hint for directions 

The goal of this exercise is to get familiar with the output of the Certora Prover, especially in case of violations, and to practice bug finding in the code.
The bugs are relatively simple and can be probably found by eye quite easily. Try not to look for the bugs manually in the implementations before you run the verification and follow the counter example. As it should be, along with the tool's result you will follow the counter example through the implementation, and try to understand where it deviates from the intended way of operation. You will then try to mitigate the problem and check it. 

Throughout each README file within this directory and its sub directories, we shall add tips and hints in collapsables to supply assistant without forcing you to take it. You will have to click on the tip actively to see it.

> :bulb: 
> <details>
>  <summary>An Expandable Tip</summary>
>  Always tip your waiters and waitresses.
></details>

</br>
For each of the systems in this directory do as follows:

</br>

- [ ] Open the interface and read the documentation and functions' signatures. The comments should get you clear on how the system should operate without going into implementation details.

</br>

- [ ] Open the spec file and go over the rules and comments there. Try to understand what the rule tries to capture and make sure that you understand this property. Look at the implementation of the rules and see if the code is clear to you.

> Make sure to read the comments at the top that explains about some new concepts that are used in the code.

</br>

- [ ] Create a script (or multiple scripts) that will serve you for running the verifications of the system's buggy versions.

> :bulb: 
> <details>
>  <summary>Script Hint</summary>
>  Craft your script wisely - use the `--rule` to filter out information that isn't of your interest.
></details>

</br>

- [ ] Run verifications of the contracts to find violations to the rules.

> :bulb: 
> <details>
>  <summary>Best Practice</summary>
>  First run the <b>entire spec</b> file against the contract you are investigating. This way you'll see which rules you need to focus on. Later you can specify a specific rule to run the contract against to save run time.
></details>

</br>

- [ ] Follow the violations as explained in [BankLesson1](../01.Lesson_GettingStarted/BankLesson1) to find out the source of the bugs.

- [ ] Fix the causes of the violations and check that the rules are really passing (green thumb up). **Be sure not to weaken the rules.**

- [ ] Save your solution to each bug in the same file that you found it in, next to the changed line(s). Mark your findings by adding a comment explaining the fix in 1-2 sentences in the following format: //@note the require checked `a > b`, when it should've checked `b > a`. 

> :bulb: 
> <details>
>  <summary>General Direction</summary>
>  Most of the bugs are in the solidity contracts, i.e. the rules are passing correctly on the "fixed version" of the code that was corrupted for this exercise.
> However, in a few specific cases, the specifications were tempered with, i.e. the rules will fail on the "fixed version" as well. 
></details>

</br>

> :bulb: 
> <details>
>  <summary>General Tip 1</summary>
> In the spec file - Try assigning variables instead of having direct function calls in expressions. By assigning variables the call trace becomes clearer and the variables' section volunteers more information.
></details>

</br>

> :bulb: 
> <details>
>  <summary>General Tip 2</summary>
> In the spec file - Try breaking complex expressions to achieve code readability and a more simplified call trace.
></details>

</br>

---

## SMT - Satisfiability Modulo Theories

</br>

- [ ] Continue to next lesson: [SMT](../03.Lesson_SMT) to learn about the underlying mechanism of the Certora Prover.

</br>

---

### Lesson 2 is all set and done. Great progress!
