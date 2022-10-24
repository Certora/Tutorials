certoraRun.exe ArrayUniqueBug.sol `
--verify ArrayUniqueBug:ArrayUniqueBug.spec `
--solc solc8.8.exe `
--send_only `
--optimistic_loop `
--loop_iter 4 `
--staging `
--rule_sanity `
--disableLocalTypeChecking `
--msg "ArrayBugSolution.sol with sanity check"