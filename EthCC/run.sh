certoraRun EthCC/ERC20.sol
    --verify ERC20:EthCC/erc20.spec \
    --staging \
    --optimistic_loop \
    --loop_iter 3 \
    --send_only \
    --msg "EthCC ERC20"