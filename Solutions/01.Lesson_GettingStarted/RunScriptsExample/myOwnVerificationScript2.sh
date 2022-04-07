certoraRun BankLesson1/Bank.sol:Bank --verify Bank:BankLesson1/Parametric.spec \
  --solc solc7.0 \
  --rule validityOfTotalFundsWithVars \
  --msg "$1"