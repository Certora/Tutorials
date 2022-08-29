if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun contracts/ERC20.sol:ERC20 \
    --verify ERC20:setup.spec \
    --optimistic_loop \
    $RULE \
    --msg "ERC20:setup.spec $1"
 