certoraRun ERC20Fixed.sol:ERC20 --verify ERC20:sanity.spec \
--solc solc8.0 \
--optimistic_loop \
--send_only \
--msg "$1" \

certoraRun ERC20VacuityBug.sol:ERC20 --verify ERC20:sanity.spec \
--solc solc8.0 \
--optimistic_loop \
--msg "$1"
