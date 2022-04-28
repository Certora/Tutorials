certoraRun contracts/Pool.sol contracts/Asset_ERC20.sol contracts/SymbolicFlashLoanReceiver.sol \
    --link Pool:asset=Asset_ERC20 \
	--verify Pool:mathProperties.spec \
    --solc solc8.0 \
    --staging \
    --rule $1 \
    --msg "Abstract Pool, mathProperties" \
    --settings -postProcessCounterExamples=true,-t=60 
#\
#    --rule $1
#   --toolOutput ../output \
#   --settings -multiAssertCheck \