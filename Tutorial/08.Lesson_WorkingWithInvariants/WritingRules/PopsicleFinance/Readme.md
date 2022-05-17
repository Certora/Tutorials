## Popsicle Finance Bug
Popsicle finance is an investment platform that acts and liquidity provider at several liquidity pools and manage to optimize gained fees for the benefit of the investor. At August 2021, a vulnerability of the Popsicle Finance smart contract SoberttoFragola was exploited, and led to a 25M$ loss of users funds.
In short, the bug is that the popsicle finance team forgot to override their default ERC20 transfer function. Look at the [attached pdf](Popsicle_Finance_Bug.pdf) description of the bug for more details. 


## How to perform the attack
Open the code in Remix IDE and perform the following steps:

1. Deploy PopsicleFinance contract.
2. User1 deposit 10 ether.
3. Owner press OwnerDoItsJobAndEarnsFeesToItsClients() and send 80 ether. User1 got 100% interest.
4. User2 deposit 10 ether.
4. User2 transfer its 10000000000000000000 tokens to User1.
5. User1 press CollectFees().
6. User1 withdraw the 20000000000000000000 tokens it holds.

User 1 ends with 30 ether more than at the begining. Although including the transfer he only deserved 20 ether more.

User2 didn't earned interest of its funds. He sent its tokens to User1 and the bug is that those tokens also accounted to User1 as tokens with 100% interest. As the default ERC20 transfer function just decrease the sender balance and increase the reciepts balance by the same ammount.

The fixed version implements transfer with the same mechanism in depoist to account interest for user only on its tokens that earned it.
