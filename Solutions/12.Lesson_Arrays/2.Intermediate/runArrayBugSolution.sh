certoraRun ArrayBugSolution.sol \
--verify ArrayBugSolution:ArrayBugSolution.spec \
--solc solc8.6 \
--send_only \
--optimistic_loop \
--loop_iter 4 \
--rule_sanity \
--msg "ArrayBugSolution.sol with sanity check"