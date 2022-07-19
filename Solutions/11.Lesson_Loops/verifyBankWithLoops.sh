certoraRun BankWithLoops.sol:Bank --verify Bank:Loops.spec \
--solc solc7.6 \
--cloud \
--optimistic_loop \
--loop_iter 2 \
--send_only \
--msg "$1"