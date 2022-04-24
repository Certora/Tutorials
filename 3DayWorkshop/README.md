
Welcome to Certora's 3 Day training. 
This training assumes knowledge in Defi: ERC20, liquidity pools.


## Day 1 -  CVL Language - Basic Rules & Understand Results

Folder ERC20 contains a generic spec for ERC20 contracts. We will use this as an example for learning CVL. We will practice running Certora Prover and understanding the results.
The folder contains a simple widely used ERC20s (Sushi, USTC, USTC, FFT) and a simple ERC20Basic contract.   

1. Go over [ERC20 spec](3DayWorkshop/ERC20/erc20.spec)
2. Run verification scripts:

    From the folder ERC20 run a script, for example:
     
     ```./scripts/verifyBasic.sh```

    
    Follow the progress of your runs in 
    [prover.certora.com](http://prover.certora.com)

3. Understand violations reported on each of the tokens:
    
    - [FFT](https://prover.certora.com/output/40726/6c78ba4a58155fd9e8fb/?anonymousKey=445e218753330d700a23d381da82002254806636)

    - [Sushi](https://prover.certora.com/output/40726/0d2cda1e5ef41c90a90d/?anonymousKey=653de68a9dd1b52acb5316d8dec51d22b575c459)

    - [USDC](https://prover.certora.com/output/40726/29ed39e35e3eb8eef2fa/?anonymousKey=605721d9efdd52fb5ebf31cb9510fc6cd2572dce)

    - [USDT](https://prover.certora.com/output/40726/19c58a5a2415580cdd26/?anonymousKey=6d284b31df55abded274d0cee387b7d84b191930)

4. Think of additional properties and write them in CVL, use ERC20Basic contract to check your rules. 
5. Check if your properties add coverage by identifying the bugs in contracts DoYouTrustMe*.sol. These contracts passed the rules in erc20.spec 

    ```./scripts/verifyDoYouTrustMe.sh```
    
    use the additional argument to run just one rule at a time:
    ```./scripts/verifyDoYouTrustMe.sh  <ruleName>```
    
7. contribute to the database of ERC20 rules by prepare a PR with additional buggy example and a rule

### Useful references
1. running scripts 
2. understanding results?  

## Day 2
