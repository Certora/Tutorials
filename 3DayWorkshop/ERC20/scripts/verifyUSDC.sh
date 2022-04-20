if [[ "$1" ]]
then
    RULE="--rule $1"
fi


certoraRun tokens/USDC.sol:FiatTokenV2_1  \
    --verify FiatTokenV2_1:erc20.spec $RULE  \
    --solc solc6.12 \
    --staging \
    --send_only \
    --optimistic_loop \
    --msg "USDC:erc20.spec $1"

certoraRun tokens/USDC.sol:FiatTokenV2_1  \
    --verify FiatTokenV2_1:erc20Answer.spec $RULE  \
    --solc solc6.12 \
    --staging \
    --send_only \
    --optimistic_loop \
    --msg "USDC:erc20Answer.spec $1"