if [[ "$1" ]]
then
    RULE="--rule $1"
fi


certoraRun tokens/ERC20Basic.sol:ERC20Basic  \
    --verify ERC20Basic:erc20.spec $RULE  \
    --solc solc8.12 \
    --staging \
    --send_only \
    --msg "Basic:erc20.spec $1"
