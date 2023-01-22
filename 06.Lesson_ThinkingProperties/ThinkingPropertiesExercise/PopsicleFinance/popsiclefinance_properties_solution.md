# Properties For PopsicleFinance

1. ***Unit tests*** deposit amount followed by withdraw amount should lead to no change in total supply and user balance of tokens
2. ***Unit tests*** user rewards should be 0 after calling collectRewards
3. ***High-level*** feesCollectedPerShare <= totalFeesEarnedPerShare
4. ***Variable transition*** totalSupply should only increase when popsicle's balance increases (deposit() should be called)
5. ***Variable transition*** totalFeesEarnedPerShare should only increase

</br>

---

## Prioritizing

</br>

### High Priority

- property 1 is high priority because if broken it can cause users to lose funds or be awarded too much funds
- property 2 is high priority because if user rewards are not 0 they can claim rewards again, potentially draining the contract
- property 4 is high priority because if token balance can increase without depositing into popsicle, then those tokens can be burned and real capital can be claimed for free. This can be used to drain the contract.
- property 5 is high priority since if someone found a way to lower the total fees, users will stop earning rewards.

### Medium Priority

- property 3 is medium priority because users might get more rewards than intended if collectedShares are more than totalShares. It can also lead to users getting less rewards than intended. This is medium priority because it does not risk other users funds.

### Low Priority
