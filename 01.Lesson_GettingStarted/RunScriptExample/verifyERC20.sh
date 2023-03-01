# format: <relative/path/to/solidity/file>:<contrac_name> --verify <contract_name>:<relative/path/to/spec/file>

certoraRun ERC20Lesson1/ERC20.sol:ERC20 --verify ERC20:ERC20Lesson1/Parametric.spec \
  --solc solc8.0 \
  --rule onlyHolderCanChangeAllowance \
  --msg "$1"

# At the end of each line a backsalsh (\) is used for line continuation - to split overly long lines.
# more on backslash before new line here: https://superuser.com/questions/794963/in-a-linux-shell-why-does-backslash-newline-not-introduce-whitespace#:~:text=The%20Backslash%2Dnewline%20is%20used,purposes%20of%20executing%20the%20script.

# The $1 is the first argument given to the script, so we can change the msg of a run without changing the actual script
# more on $1 here: https://bash.cyberciti.biz/guide/$1