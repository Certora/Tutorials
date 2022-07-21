certoraRun LiquidityPool.sol Asset_ERC20.sol SymbolicFlashLoanReceiver.sol \
    --link LiquidityPool:asset=Asset_ERC20 \
	--verify LiquidityPool:pool.spec \
    --solc solc8.0 \
    --cloud  \
    --msg "Liquidity Pool:  $1 " \
