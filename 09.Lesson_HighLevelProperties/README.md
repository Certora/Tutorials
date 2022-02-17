# Some More Thinking About Properties

In this Lesson, after you've already practiced coming up with meaningful properties, we raise the bar with slightly more sophisticated contracts and focus on high-level properties.

> :information_source: Remember, high-level properties are properties that try to look at the big picture rather than a specific detail. An example to a high-level rule would be: "In a bank, a user can withdraw his/her rightful funds from the account." i.e. the bank suppose to allow withdrawal of funds that exist in the account at all time, but also no action from a 3rd party can prevent the user from withdrawing their funds.

> :warning: Note that transfer by approved 3rd party will change the account's balance legitimately.

High-level properties are usually implemented as invariants or parametric rules, as oppose to rules that monitor the behavior of the system as a result of a specific function call. The latter will very rarely represent high-level rules, due to its diminished "attack vector" possibility.

- [ ] Follow the instructions on [Thinking Properties Exercise](ThinkingPropertiesExercise) to exercise some more on coming up with properties, categorizing them, and prioritizing them.

</br>

- [ ] Create a `.spec` file for [Borda Election](ThinkingPropertiesExercise/Borda) and [ERC20](ThinkingPropertiesExercise/ERC20), and try to prove 5 properties in each of them based on your properties.

Upload your solutions to the directories to get review by the Certora team.

</br>


---

## Working With Invariants

</br>

- [ ] Continue to the next lesson: [Vacuous Rules](../10.Lesson_VacuousRules) to learn about vacuous rules, how to avoid them, and how to catch them on time.

</br>

---

### “Man is still the most extraordinary computer of all.” - John F. Kennedy.

---
