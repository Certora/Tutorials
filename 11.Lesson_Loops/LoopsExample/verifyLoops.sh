solc-select use 0.8.11
certoraRun Loops.sol:Loops --verify Loops:LoopsUnrolling.spec \
--solc solc \
--loop_iter 3 \
--send_only \
--msg "loop iter 3 no optimism"

certoraRun Loops.sol:Loops --verify Loops:LoopsUnrolling.spec \
--solc solc \
--loop_iter 5 \
--send_only \
--msg "loop iter 5 no optimism"

certoraRun Loops.sol:Loops --verify Loops:LoopsUnrolling.spec \
--solc solc \
--loop_iter 10 \
--send_only \
--msg "loop iter 10 no optimism"