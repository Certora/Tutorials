certoraRun ArrayImproved.sol \
--verify Array:Array.spec \
--solc solc8.6 \
--send_only \
--optimistic_loop \
--loop_iter 4 \
--staging \
--rule_sanity \
--msg "Array.sol with sanity check"
