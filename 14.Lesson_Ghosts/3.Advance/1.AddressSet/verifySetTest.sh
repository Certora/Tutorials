certoraRun setTest.sol:SetTest  \
    --verify SetTest:EnumerableSet.spec \
    --solc solc8.10 \
    --loop_iter 3 \
    --rule_sanity \
    --staging \
    --optimistic_loop \
    --settings -mediumTimeout=1200,-adaptiveSolverConfig=false,-useBitVectorTheory,-showInternalFunctions \
    --send_only \
    --msg "14.Lesson_Ghosts 3.Advance ALL timeout 1200"