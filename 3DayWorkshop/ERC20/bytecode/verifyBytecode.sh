if [[ "$1" ]]
then
    RULE="--rule $1"
fi
cp ../erc20.spec .
certoraRun --bytecode DoYouTrustMe1.json --bytecode_spec erc20.spec --staging --send_only --msg "doYouTrustMe1:erc20.spec  "
certoraRun --bytecode DoYouTrustMe2.json --bytecode_spec erc20.spec --staging --send_only  --msg "doYouTrustMe2:erc20.spec  "

