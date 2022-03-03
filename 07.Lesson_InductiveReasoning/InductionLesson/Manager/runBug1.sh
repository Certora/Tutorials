solc-select use 0.8.6

certoraRun ManagerBug1.sol:Manager --verify Manager:ManagerSolution.spec \
--solc solc \
--send_only \
--msg "$1"