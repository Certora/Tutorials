if [[ "$1" ]]
then
    RULE="--rule $1"
fi


certoraRun tokens/FTT.sol:FTT  \
    --verify FTT:erc20.spec $RULE  \
    --solc solc5.3 \
    --cloud \
    --send_only \
    --optimistic_loop \
    --msg "FTT:erc20.spec $1"