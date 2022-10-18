certoraRun pay.sol:pay  \
    --verify pay:pay.spec \
    --solc solc8.10 \
    --loop_iter 2 \
    --rule_sanity \
    --optimistic_loop \
    --settings -adaptiveSolverConfig=false,-useBitVectorTheory,-showInternalFunctions \
    --send_only 
