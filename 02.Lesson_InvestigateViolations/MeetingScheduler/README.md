# Hints for MeetingScheduler\

<details>
<summary>General Hint 1:</summary>
There are 2 rules that are failing regardless of the implementation. They will fail on the correct implementation as well. Can you spot them?
The next general hints will refer to these rules.
</details>

</br>

<details>
<summary>General Hint 2:</summary>
Run the rule <code>checkStartedToStateTransition</code> on one of the implementations that you've already fixed. It still fails.
Follow the values in the assertion closely, particularly the explicit values of the states, are they checking what the rule wants them to check?
</details>

</br>

<details>
<summary>General Hint 3:</summary>
Run the rule <code>monotonousIncreasingNumOfParticipants</code> on one of the implementations that you've already fixed. It still fails.
Look at the failing method, how come before creating a meeting the number of participants was greater than 0? Go back to BankLesson1 and refresh yourself about the failure in <code>TotalGreaterThanUser.spec</code> and its mitigation (precondition).
</details>

</br>

## MeetingSchedulerBug1.sol
<details>
<summary>Hint:</summary>
What's the assert failing here on the rule <code>startOnTime</code>? 
What are the variables that are checked against each other in the inequalities and what are their values?
</details>

</br>

## MeetingSchedulerBug2.sol
<details>
<summary>Hint:</summary>
Why is the assertion failing on <code>endMeeting</code>? Are the <code>uint8</code> values of the enumerable match their expected values?
</details>

</br>

## MeetingSchedulerBug3.sol
<details>
<summary>Hint:</summary>
In the world of MeetingScheduler, the shortest meeting is at least 1 second. What are the values of the variables checked in the assertion?
</details>

</br>

## MeetingSchedulerBug4.sol
<details>
<summary>Hint 1:</summary>
Before you fix the code you need to find another problem that lies in another file.
See General Hints 1 + 2 for more help on that.
</details>

</br>

<details>
<summary>Hint 2:</summary>
Now that you've fixed the problem with the rule, does it make sense that the condition fails on <code>joinMeeting</code>?
</details>
