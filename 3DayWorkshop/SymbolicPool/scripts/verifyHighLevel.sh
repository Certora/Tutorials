if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun contracts/Pool.sol contracts/Asset_ERC20.sol contracts/SymbolicFlashLoanReceiver.sol \
    --link Pool:asset=Asset_ERC20 \
	--verify Pool:highLevel.spec $RULE \
    --solc solc8.0 \
    --staging  \
    --msg "Abstract Pool, highLevel.spec multiAssertCheck  " \
    --settings -multiAssertCheck 
#\
#    --rule $1
#   --toolOutput ../output \
#   --settings -multiAssertCheck \