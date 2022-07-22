if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun LiquidityPool.sol Asset_ERC20.sol SymbolicFlashLoanReceiver.sol \
    --link LiquidityPool:asset=Asset_ERC20 \
	--verify LiquidityPool:pool.spec \
    --solc solc8.0 \
    --cloud  \
    $RULE \
    --msg "Liquidity Pool:  $1 " \
