certoraRun contracts/ERC20.sol:ERC20 \
    --verify ERC20:setup.spec \
    --optimistic_loop \
    --msg "ERC20:setup.spec $1"
 