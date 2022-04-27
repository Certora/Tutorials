if [[ "$1" ]]
then
    RULE="--rule $1"
fi


certoraRun tokens/USDT.sol:TetherToken  \
    --verify TetherToken:erc20.spec $RULE  \
    --solc solc4.25 \
    --cloud \
    --send_only \
    --optimistic_loop \
    --msg "USDT:erc20.spec $1"

