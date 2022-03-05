solc-select use 0.7.6

certoraRun BankWithLoops.sol:Bank --verify Bank:Loops.spec \
--solc solc \
--optimistic_loop \
--loop_iter 3 \
--send_only \
--msg "check"