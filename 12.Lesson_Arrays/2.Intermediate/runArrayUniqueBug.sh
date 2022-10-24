<<<<<<< HEAD
certoraRun ArrayBug.sol `
--verify ArrayBug:ArrayBugSolution.spec `
--solc solc8.6 `
--send_only `
--optimistic_loop `
--loop_iter 4 `
--staging `
--rule_sanity `
--disableLocalTypeChecking `
--msg "ArrayBugSolution.sol with sanity check"
=======
certoraRun ArrayUniqueBug.sol \
--verify ArrayUniqueBug:ArrayUniqueBug.spec \
--solc solc8.6 \
--send_only \
--optimistic_loop \
--loop_iter 4 \
--staging \
--rule_sanity \
--msg "ArrayUniqueBug.sol with sanity check"
>>>>>>> 70096b7988cbff55906cc191bd8c8b8bbe30eafd
