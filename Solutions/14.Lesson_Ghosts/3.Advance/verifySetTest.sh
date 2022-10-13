certoraRun setTest.sol:SetTest  \
    --verify SetTest:set.spec \
    --solc solc8.10 \
    --loop_iter 5 \
    --optimistic_loop \
    --settings -adaptiveSolverConfig=false,-useBitVectorTheory,-showInternalFunctions \
    --send_only 
