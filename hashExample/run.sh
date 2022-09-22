certoraRun hashExample/Offchain.sol \
    --verify Offchain:hashExample/offchain.spec \
    --solc solc8.6 \
    --staging \
    --settings -byteMapHashingPrecision=12 \
    --send_only \
    --rule_sanity basic