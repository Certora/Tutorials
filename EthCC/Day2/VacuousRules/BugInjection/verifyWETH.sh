certoraRun WETH.sol:WETH9 --verify WETH9:weth.spec \
--solc solc4.25 \
--optimistic_loop \
--rule_sanity \
--msg "$1" \
