# This script is iterating over every contract that's needed to be verified
# and run the sanity spec file against it.
for f in certora/harnesses/Wizard*.sol
do
    echo "Processing $f"
    file=$(basename $f)
    echo ${file%.*}
    certoraRun certora/harnesses/$file \
    --verify ${file%.*}:certora/specs/sanity.spec "$@" \
    --solc solc8.2
    --optimistic_loop \
    --msg "checking sanity on ${file%.*}"
    --settings -copyLoopUnroll=4
done