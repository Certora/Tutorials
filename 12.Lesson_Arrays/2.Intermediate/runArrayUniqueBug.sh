certoraRun ArrayUniqueBug.sol \
--verify ArrayUniqueBug:ArrayUnique.spec \
--solc solc8.6 \
--send_only \
--staging master \
--optimistic_loop \
--loop_iter 4 \
--rule_sanity \
--msg "ArrayUniqueBug.sol with sanity check"
