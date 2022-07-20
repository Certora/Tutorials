if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun contracts/FiatTokenV2_1.sol:FiatTokenV2_1 \
    --verify FiatTokenV2_1:specs/erc20.spec \
    --cloud \
    --solc solc6.12 \
    --optimistic_loop \
    --loop_iter 3 \
    $RULE \
    --send_only \
    --msg "EthCC ERC20 DontSellMe: $1 $2"
