# Properties For Auction

We took some time to study the system, ask questions, discuss with each other on the way it operates and came up with the following properties.
First, let us define the states of the system:

```ruby
- `defNonCreated` - (Non created/Closed) is defined as `auctions[id].end_time` is 0.
- `defCreated` - (Created/Started) is defined as `auctions[id].end_time` is not 0.
```

1. ***Valid state*** - `defNonCreated` => `getAuction(id)` returns all 0s. If auction values are not 0 then one can get benefits from auction multiple times, which isn't not acceptable.

2. ***Valid state*** - `defCreated` => `auctions[id].winner != 0`. If winner is 0 then nobody will get the auction prize.

3. ***Variable transition*** - `defCreated` => prize cannot be increased. Otherwise, an attacker can change the prize value to either deny winner from getting any reward or reward the winner with more than reward than intended. 

4. ***Variable transition*** - `defCreated` => `auctions[id].bid_expiry` cannot be decreased. If the expiry can be tempered (i.e. be decreased in value) then an attacker can raise an offer, set the expiry date to the past and close the auction before anyone is able to offer a counter offer. A failure here will create a possibility to rig auctions.

5. ***Variable transition*** - `balanceOf(auctions[id].winner)` was increased => `user` == `auctions[id].winner` && `close()` was called. We check that there is no other way to increase user's balance inside system except to become a winner and call `close()` method. We don't consider external transfers.

6. ***Variable transition*** - If after a call to some method while in `defCreated` state, `getAuction(id)` returns all 0's, then the call method was `close()`. If it is possible to delete an auction's details by calling any other function it can cause a DoS attack.

7. ***High-level*** - No way to delete an auction if `auctions[id].bid_expiry == 0` or `(auctions[id].bid_expiry >= now || auctions[id].end_time >= now)`. Once an auction is active there is no way to shut it. This property also aims to prevent DoS attacks.

8. ***High-level*** - Solvency - Total supply of tokens is greater or equal to the sum of balances of all users. The system has enough tokens to pay everyone what the deserve.

9. ***Unit tests*** - mint() correctly increases `balances[who]` and `totalSupply`.

10. ***Unit tests*** - transferTo() correctly increases `balances[_to]` and correctly decreases `balances[msg.sender]`.

</br>

---

## Prioritizing

</br>

Once the list of properties is finished, the team meet to discuss it. Each property is explained by its creator to the others, and either being approved, denied or refined.
With every property the team discuss the implications of the property failing, and prioritize them accordingly.

Here is a summary of our prioritization:

### High Priority:

- Property 1 is high priority because user can win the auction and get benefits only once by initial intention. Moreover, `mint()` increases a value of `totalSupply` that can block other auctions to finish if you can claim prize multiple times.

- Properties 2 & 5 are high priority because if they fail the winner will not get his/her deserved reward which fails the entire idea of this system.

- Property 3 is high priority because `mint()` increases a value of `totalSupply` that can block other auctions to finish if you can claim huge prize. Also we want to prevent attacker from getting additional benefits.

- Properties 4 & 7 are high priority because violation of this rule means that attacker can unjustly win an auction without any competition (kind of DoS).

- Property 6 is high priority because we want to prevent DoS attack. Otherwise, there is no reason to participate in such auction.

### Medium Priority:

- Property 8 is medium priority only because there is no withdraw method that could decrease totalSupply to 0 and prevent people from getting their tokens. Otherwise, it's high priority.

### Low Priority:

- Properties 9 & 10 are low priority since:
    1. They check implementation of a specific function (as oppose to multiple functions).
    2. They fairly simple to check by other means, including by manual reviewing of the code.