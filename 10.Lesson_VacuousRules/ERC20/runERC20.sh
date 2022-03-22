solc-select use 0.8.0;

certoraRun ERC20Bug1.sol:ERC20 --verify ERC20:ERCVacuity.spec \
--solc solc \
--send_only \
--optimistic_loop \
--msg "check all tautologies"