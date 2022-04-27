if [[ "$1" ]]
then
    RULE="--rule $1"
fi


certoraRun tokens/doYouTrustMe1.sol:ERC20Basic  \
    --verify ERC20Basic:erc20.spec $RULE  \
    --solc solc8.12 \
    --cloud \
    --send_only \
    --optimistic_loop \
    --msg "doYouTrustMe1:erc20.spec $1"

certoraRun tokens/doYouTrustMe2.sol:ERC20Basic  \
    --verify ERC20Basic:erc20.spec $RULE  \
    --solc solc8.12 \
    --cloud \
    --send_only \
    --optimistic_loop \
    --msg "doYouTrustMe2:erc20.spec $1"