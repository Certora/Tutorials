# Harness

It is no secret that the Certora Prover still has limitations. Take the [Borda](Borda) system for example - there is no way to approach the struct fields defined in the interface straight from the spec file.


- eco system - symbolic ERC20, flashloan receiver
- summarization
- simplify complexity for the tool

Often we need to gain access 

> :bulb: As it stands, harness is a "necessary evil", however, it is important to note that it's also a ***temporary evil***. The Certora development team is working on making harness a thing of the past. In the near future you'll be able to gaining safe access to variables and methods with a `private` modifier, as well as generating multiple instances of the same contract.

---
## Exercise

---

### Borda Election

</br>

In the [Borda directory](Borda) you will find the Borda Election system we've been working on throughout the course.
This implementation of the system is stripped from most of its public getters to resemble a real live system (without unnecessary public getters for each field).

- [ ] Create a harness contract and fill it with any functions needed for verifying the set of properties listed in the next bullet.

- [ ] Implement the following list properties, and verify your `.spec` file against the harness contract you've created.

    - [ ] Any voter that had cast his vote already is marked as registered.

    - [ ] Voters that are marked as Black Listed has at least 3 votes attempts.

    - [ ] Voters that has at least 3 vote attempts recorded are marked black listed.

    (hint: properties 2 & 3 can be merged into 1 property )

    - [ ] Monotonicity of points - number of total distributed points is non decreasing (hint: ghost).

    - [ ] Monotonicity of points 2 - number of contender's points is non decreasing (hint: ghosts).

    - [ ] Monotonicity of voters - number of voters that has voted is non decreasing (hint: ghosts).

    - [ ] TODO: The number of registered voters is always greater or equal to the number of voters that has voted (hint: ghosts).

    - [ ] A single contender's point count is smaller than total point count (hint: ghosts)

    - [ ] In each successful vote casting, exactly 6 points are being distributed (hint: ghosts).

    - [ ]  The total number of points casted divided by 6 equals to the number of voters casted their votes (hint: ghosts).

Upload your solution to the [Borda directory](Borda) for review by the Certora team.

</br>

---

## Very Last Lesson

</br>

- [ ] Continue to next lesson: [Relational Properties](../17.Lesson_RelationalProperties) to learn about quantifiers, and timeouts.

</br>

---

### “The advance of technology is based on making it fit in so that you don't really even notice it, so it's part of everyday life.” - Bill Gates

---
