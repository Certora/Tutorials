if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun contracts/DontSellMe.sol:DontSellMe \
    --verify DontSellMe:specs/erc20.spec \
    --cloud \
    --solc solc8.15 \
    --optimistic_loop \
    --loop_iter 3 \
    $RULE \
    --send_only \
    --msg "EthCC ERC20 DontSellMe: $1 $2"
