certoraRun.exe Array.sol `
--verify Array:Array.spec `
--solc solc8.8.exe `
--send_only `
--optimistic_loop `
--loop_iter 4 `
--staging `
--rule_sanity `
--disableLocalTypeChecking `
--msg "Array.sol with sanity check"