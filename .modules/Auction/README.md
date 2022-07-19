# Guided Exercise - Liquidity Pool With Flash Loans

This demonstration shows how a generic rule can detect a real bug.
This example is based on a real bug found in the "Flop Action" contract of Maker MCD by the Certora Prover.

You can read about the catch in the following [blog post](https://blog.makerdao.com/mcd-security-roadmap-update-october-2019/)


- [ ] Look at the contract [Auction Fixed](AuctionFixed.sol) in this directory created by Maker. Try to understand what the contracts do and how they operate in a high-level sense.
    
</br>

- [ ] Try to think about as many properties as you can for the contract. Write them down in your favorite word processor and upload them in a file named "auction_properties_solution" to the current directory.

</br>

- [ ] Go over the list of properties in [properties List](propertiesList.md) to see an example of a preparation to a verification project. The properties are categorized, prioritized, and fully detailed to explain the essence of the property in a few sentences or logic.

</br>

- [ ] Have a look at the prepared `.spec` file [Auction](Auction.spec) and try to read the properties. Some commands there are using the old syntax of CVL which is still supported, don't worry if you do not understand everything.

</br>

- [ ] Go back to your set of properties and see if you have any additional ideas after reading the example list. Make sure to upload your changes.

- [ ] If possible, reach out to a fellow participant of the onboarding course and discuss your properties with them. Exchange thoughts and ideas.

</br>

> :memo: The Certora Team will review your solution and give you a personal review. In the following days, you will exercise thinking about properties some more; we recommend waiting for your review before proceeding to the next exercise in this subject.

</br>

- [ ] Run the script [runBroken.sh](runBroken.sh) and get a violation. Investigate the reason for the fail and see that you understand it.

- [ ] Try to suggest a solution that will mitigate the wrongful behavior.

- [ ] Compare the 2 contracts - [Auction Broken](AuctionBroken.sol) and [Auction Fixed](AuctionFixed.sol) to find the fix. Run the script [runFixed.sh](runFixed.sh) and see that it is indeed solving the problem.
Were you thinking of the same solution or did you think of another one? There could be more than 1 correct answer.