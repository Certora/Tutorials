if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun .modules/ERC20/ERC20Fixed.sol:ERC20 \
    --verify ERC20:EthCC/erc20.spec \
    --staging \
    --optimistic_loop \
    --loop_iter 3 \
    $RULE \
    --send_only \
    --msg "EthCC ERC20: $1"