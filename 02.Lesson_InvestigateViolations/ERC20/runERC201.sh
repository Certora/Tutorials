solc-select use 0.8.0
certoraRun ERC20Bug1.sol:ERC20 --verify ERC20:ERC20.spec \
--solc solc \
--optimistic_loop \
--send_only \
--msg "$1"