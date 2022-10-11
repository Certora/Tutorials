certoraRun Array.sol \
--verify Array:array.spec \
--solc solc8.6 \
--send_only \
--optimistic_loop \
--loop_iter 4 \
--staging \
--rule_sanity \
--msg "array.sol with sanity check"