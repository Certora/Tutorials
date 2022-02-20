# Declaring Methods, Creating Definitions and Using CVL Functions

## Methods

</br>

In CVL, you can call `external` and `public` methods from the verified contract (or other contracts in the verification context) as they are automatically declared. The default declaration assumes that the methods require the calling context (`env`) to work properly and urges you to send it as an argument. 

> :information_source: You can see that every function call in Lesson 1 included an `env` argument. If we had removed the `env` argument from the function call, an error would've risen in the local type-checking phase.

However, the calling context (sender, value, timestamp, block number, etc.) is not always crucial for a function's operation. Take the `view` function `getFunds()` in [Bank](LessonExamples/Methods.sol) as an example:

```
	function getFunds(address account) public view returns (uint256) {
		return funds[account];
	}
```

There is no need for any Ethereum-frame context to retrieve the funds of a specified HEX address from the system.
For these cases, one can create a `methods` block and explicitly declare the functions they will use in the spec. The declaration is similar to a function declaration in a Solidity interface. At the end of the declaration, one can specify the function as `envfree`, meaning it does not depend on the context, so no `env` variable should be expected in the function call. If `envfree` isn't specified at the end, the function will require an `env` argument (equivalent to not declaring it).

- [ ] Have a look at the methods block in the altered, yet familiar spec from Lesson 1 - IntegrityOfDeposit: [BankFixed.sol](LessonExamples/BankFixed.sol) and [Methods_IntegrityOfDeposit.spec](LessonExamples/Methods_IntegrityOfDeposit.spec)

In general, creating an arbitrary `env` variable and passing it to the function call does not affect verification results. Still, we recommend declaring functions as `envfree` whenever possible to write cleaner and less confusing code.

Another reason to declare functions, even if they aren't `envfree`, is to make the specification more self-contained and readable. 

- [ ] Read the documentation on [method declarations](https://certora.atlassian.net/wiki/spaces/CPD/pages/181960777/Method+Declarations) up to "Summary Declarations" (not including). Notice that the documentation refers to things that we haven't learned yet. Don't worry; we will get to it in the future.

This directory contains the three systems from the Lesson 1 Exercise. The interface implementations are the fixed versions (all the rules pass on them out of the box).

- [ ] Write a methods block for each spec and declare as `envfree` every possible function.

- [ ] Run the verification to make sure that your declarations work. You should get a verification report where all rules are passing.

</br>

---

## CVL Functions

</br>

Like any other programming language, CVL provides a way to encapsulate code in functions for convenient code reuse.

- [ ] Read the documentation on [CVL functions](https://certora.atlassian.net/wiki/spaces/CPD/pages/238846033/CVL+Functions). 

- [ ] Have a look at the CVL functions in the altered, yet familiar spec from Lesson 1 - `TotalGreaterThenUser`: [BankFixed.sol](LessonExamples/BankFixed.sol) and [Functions_TotalGreaterThenUser.spec](LessonExamples/Functions_TotalGreaterThenUser.spec)

These are plain, simple, and perhaps even silly examples of CVL functions that one may not implement in a real specification. Keep in mind that these examples are simply there to get you going on features of the CVL and their syntax. You will write more useful functions soon enough.

- [ ] Write CVL functions in [Borda Election](Borda) that takes a voter as argument and retrieves just one element from the struct, i.e. age, registered, voted, etc.

> :bulb: 
> <details>
>  <summary>Hint</summary>
> Look at the use of `getFullVoterDetails` in `onceBlackListedNotOut`. you can export this assignment to a CVL function that will retrieve a single element that you need.
></details>

- [ ] Have a look at the other systems to see if you can find another place where CVL functions can come in handy.

- [ ] Run the verification to make sure that your declaration works. You should get a verification report where all rules pass.

---

## Definitions

</br>

Definitions are [macros](https://en.wikipedia.org/wiki/Macro_(computer_science)) that we can declare at the top-level of a specification. These macros are available in the scope of every rule, function, and other definitions.
Definitions are usually used for one of 2 purposes:

1. Declaring a constant. For example, the speed of light is `299,792,458 m/sec`. It can be declared globally as follows:

```
definition C() returns uint256 = 299792458;
``` 

</br>

2. Declaring a global expression that is useful throughout the entire spec, e.g., declaring a state of the system or a variable within the system. We can take [MeetingScheduler](MeetingScheduler) as an example and declare one of its states:

```
definition meetingUninitialized(uint256 meetingId) returns bool = getStartTimeById(meetingId) == 0 && getEndTimeById(meetingId) == 0 && ...;
```

- [ ] Read the documentation on [definitions](https://certora.atlassian.net/wiki/spaces/CPD/pages/41156868/Definitions) up to "Reference Ghost Functions" (not including).

- [ ] Write the definitions of all the states in the [MeetingScheduler](MeetingScheduler) system.

- [ ] Try writing a few definitions for a voter in [Borda](Borda) contract:
1. `unRegisteredVoter` - for a voter that isn't registered at all.
2. `registeredYetVotedVoter` - for a registered voter that hasn't voted yet.
3. `legitRegisteredVotedVoter` - for a registered voter that has voted but isn't blocked.
4. `blockedVoter` - for a registered voter that has voted, and is blocked.
- [ ] Use the CVL function for that task.

- [ ] Have another look at the other systems and think if you can create useful definitions for them.

- [ ] Run the verification to make sure that your declarations work. You should get a verification report where all rules pass.
