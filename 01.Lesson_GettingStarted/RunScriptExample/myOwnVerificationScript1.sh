solc-select use 0.7.5
certoraRun ./BankLesson1/Bank.sol:Bank --verify Bank:./BankLesson1/TotalGreaterThanUser.spec \
  --solc solc
  --msg "My first Certora shell script"