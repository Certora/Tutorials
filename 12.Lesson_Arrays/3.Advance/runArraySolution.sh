certoraRun ArraySolution.sol \
--verify ArraySolution:ArraySolution.spec \
--solc solc8.6 \
--send_only \
--optimistic_loop \
--loop_iter 4 \
--staging \
--rule_sanity \
--msg "ArraySolution.sol with sanity check"