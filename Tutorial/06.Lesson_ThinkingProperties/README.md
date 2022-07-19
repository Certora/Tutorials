# A Guide For Thinking About Properties

Now that we've had an introduction to Certora Prover's underlying mechanism, and after we've got a taste of how it
may benefit us, it's time to learn about the first step of Formal Verification (FV) - thinking about systems' properties and defining systems' specifications.

In auditing, you first need to get familiar with the system in question. In this phase, the auditor understands the high-level design of the system - how it is supposed to work and behave, without diving into implementation details. This phase should come before we start looking for concrete bugs.
Doing that helps spot lines of code that cause deviation from the expected behavior of the system in the next phase.

The same goes for formal verification. Before we start thinking about rules, we need to get familiar with the system. Once we know how the system is expected to behave, we can start thinking about its properties - requirements that the system must follow.
This set of requirements is called [specification](https://en.wikipedia.org/wiki/Formal_specification).

The recommended way to create a specification file is to first express each system requirement in your preferred language (english/pseudo code), then try to reason about it, refine it, and even express it in a more precise mathematical/logic language.
Obviously, you can go straight away to write the property in mathematical form. However, it isn't always a simple task so when you have a hard time formulating a logical expression, go back to defining it in free language.

Although this step may seem obvious or cumbersome, 
we cannot stress enough how important it is. 
Coming up with meaningful properties is the most challenging part of the work. 
Without the ability to identify and express meaningful properties, 
all your technical knowledge with the tool is worthless. 
Even the most skillful security engineer will contribute nothing to a system's security if:

1. The property they try to prove is wrong (will never be proved and show unhelpful counter examples).

2. The property they are proving is very local and have partial coverage. In which case many potential bugs will not be detected with this property. 

3. The property is already covered by another property

4. The property is mimicking the implementation, i.e., copying `requires` from the implementation instead of defining a correct high level specification. This is a common and dangerous mistake because if the implementation deviates from its intended purpose the verification will not find it, but rather verify that the implementation works wrong.

The process of coming up with properties and rules ideas is not done once you start the verification.
You will find out that it is an iterative process. While writing rules, you will better understand the system through violations of your properties and discover more rules and invariants that you can and need to define in the specification.

- [ ] Go through the presentation [Categorizing Properties](Categorizing_Properties.pdf) to learn about different classes of properties that can be found in real-life systems.

</br>

- [ ] Follow the instructions in [AuctionDemonstration](AuctionDemonstration) to have a guided exercise with a demonstration of thinking about properties.

</br>

- [ ] Follow the instructions on [Thinking Properties Exercise](ThinkingPropertiesExercise) to exercise some more on coming up with properties, categorizing them, and prioritizing them.

</br>

- [ ] Create a `.spec` file for [MeetingScheduler](ThinkingPropertiesExercise/MeetingScheduler) and [TicketDepot](ThinkingPropertiesExercise/TicketDepot), and try to prove 5 properties in each of them based on your properties.

Upload your solutions to the directories to get review by the Certora team.

</br>

---

## Conclusion

</br>

In this lesson you've learned the most critical stage of work with the Certora Prover: writing specifications.
Don't underestimate the importance of this phase. Formal verification is worthless without meaningful properties.

</br>

---

## Inductive Reasoning

</br>

- [ ] Continue to next lesson: [Inductive Reasoning](../07.Lesson_InductiveReasoning) to learn about inductive reasoning and the use of invariants.

</br>

---

### "One machine can do the work of fifty ordinary men. No machine can do the work of one extraordinary man." - Elbert Hubbard

---
