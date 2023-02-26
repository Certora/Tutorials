certoraRun ArraySolution.sol `
--verify ArraySolution:ArraySolution.spec `
--solc solc8.8 `
--send_only `
--optimistic_loop `
--loop_iter 3 `
--staging `
--rule_sanity `
--disableLocalTypeChecking `
--msg "ArraySolution.sol with sanity check"