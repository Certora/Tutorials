certoraRun ./BankLesson1/Bank.sol:Bank --verify Bank:./BankLesson1/Parametric.spec \
  --solc solc \ # This is solc instead of solc<version> because I use solc-select and the path stays as just "solc" when I use a different compiler. 
  --rule validityOfTotalFundsWithVars \
  --msg "My second Certora shell script"