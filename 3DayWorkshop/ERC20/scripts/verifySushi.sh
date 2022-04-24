if [[ "$1" ]]
then
    RULE="--rule $1"
fi


certoraRun tokens/Sushi.sol:SushiToken  \
    --verify SushiToken:erc20.spec $RULE  \
    --solc solc6.12 \
    --cloud \
    --send_only \
    --optimistic_loop \
    --msg "Sushi:erc20.spec $1"