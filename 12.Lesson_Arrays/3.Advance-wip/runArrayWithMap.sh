certoraRun ArrayWithMap.sol \
--verify ArrayWithMap:ArrayWithMap.spec \
--solc solc8.6 \
--send_only \
--optimistic_loop \
--loop_iter 4 \
--rule_sanity \
--msg "ArrayWithMap.sol with sanity check"