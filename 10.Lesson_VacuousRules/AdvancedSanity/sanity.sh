if test -n "$1"
then
    RULE="--rule $1"
fi
certoraRun ./sanity.sol:sanityCheck \
\
\
--verify sanityCheck:./sanity.spec \
--solc solc8.0 \
--send_only \
--staging \
--rule_sanity advanced \
$RULE \
--msg "sanity check $1 -- $2" \

# ./contracts/data-verification-mechanism/implementation/Store.sol \