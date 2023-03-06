certoraRun verification/harnesses/SymbolicVault.sol verification/harnesses/MultiDistributorHarness.sol \
  verification/harnesses/SymbolicERC20A.sol verification/harnesses/SymbolicERC20B.sol \
  --verify MultiDistributorHarness:verification/specs/multiDistributorRules.spec \
  --solc solc7.6 \
  --rule transition_DistFinished_To_DistActive \
  --rule_sanity \
  --optimistic_loop \
  --settings -postProcessCounterExamples=true \
  --packages @balancer-labs/v2-solidity-utils=pkg/solidity-utils @balancer-labs/v2-vault=pkg/vault \
  --msg "$1"
  