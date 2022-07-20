if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun EthCC/ERC20/contracts/ERC20.sol:ERC20 \
    --verify ERC20:EthCC/ERC20/specs/erc20.spec \
    --cloud \
    --optimistic_loop \
    --loop_iter 3 \
    $RULE \
    --send_only
