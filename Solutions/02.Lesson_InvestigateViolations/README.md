# Implemented Bugs:

## Borda

1. Bug1 - in `vote()` all contenders get 3 points by calling `voteTo()` with 3 points for all contenders.
2. Bug2 - `registerVoter()` 1st requirement checks that the sender is registered as contender.
3. Bug3 - the 1st line in `voteTo()` does not use safe add - this is the line that calculates the new point count of the specified contender.
4. Bug4 - After a voter votes successfully, right before the update of the struct, the registered boolean is changed to false.

## Meeting Scheduler

1. Bug1 - line 74 was removed (`require block.timestamp >= scheduledMeeting.startTime`).
2. Bug2 - switched the name of functions `endMeeting()` and `cancelMeeting()` - when calling to `endMeeting()` the implementation of `cancelMeeting()` is being invoked and vice versa
3. Bug3 - line 58 - `startTime` is allowed to be equal to `endTime` (now `>=` instead of `>`)
4. Bug4 - At the end of `joinMeeting()` a deliberate status change to `ENDED` was added. 

## ERC20

1. Bug1 - `increaseAllowance()` is now decreasing allowance (            `_allowances[msg.sender][spender] + addedValue` to             `_allowances[msg.sender][spender] - addedValue`)
2. Bug2 - in `_transfer()` the require that checks `sender.balance>=amount` was removed, and the calculation remained `unchecked`.
3. Bug3 - added the line `_balances[spender] = amount` in `_approve`.
4. Bug4 - in `transferFrom()` the require was removed (similar to Bug2) and `_approve()` was changed in the allowance update to be `amount * 9`.
5. Bug5 - last rule in the spec (5th) - is failing the fixed version as well, is it worth giving it as an exercise to understand whats wrong?

Issue - `balanceChangesFromCertainFunctions()` is failing on getters.