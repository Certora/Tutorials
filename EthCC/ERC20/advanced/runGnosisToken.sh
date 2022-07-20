if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun contracts/GnosisToken.sol:GnosisToken \
    --verify GnosisToken:specs/erc20.spec \
    --cloud \
    --solc solc4.24 \
    --optimistic_loop \
    --loop_iter 3 \
    $RULE \
    --send_only \
    --msg "EthCC ERC20 DontSellMe: $1 $2"
