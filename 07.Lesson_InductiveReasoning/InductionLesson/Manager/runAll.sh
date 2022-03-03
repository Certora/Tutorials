solc-select use 0.8.6

certoraRun Manager.sol:Manager --verify Manager:ManagerSolution.spec \
--solc solc \
--send_only \
--msg "Manager"

certoraRun ManagerBug1.sol:Manager --verify Manager:ManagerSolution.spec \
--solc solc \
--send_only \
--msg "Manager Bug 1"

certoraRun ManagerBug2.sol:Manager --verify Manager:ManagerSolution.spec \
--solc solc \
--send_only \
--msg "Manager Bug 2"