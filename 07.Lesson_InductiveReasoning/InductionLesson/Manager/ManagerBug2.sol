
contract Manager {

	struct ManagedFund {
        // The current manager of the fund
        address currentManager;
        // Management can be transferred, however the new manager needs to claim the management after being set as pending manager.
        address pendingManager;
		// amount managed
		uint256 amount;
	}

	// Maps a fundId to its struct
	mapping (uint256 => ManagedFund) public funds; 

	// A flag indicating if an address is a current manager
	mapping (address => bool) public isActiveManager; 


	function createFund(uint256 fundId) public {
		require(msg.sender != address(0));
		require(funds[fundId].currentManager == address(0));
		require(!isActiveManager[msg.sender]);
		funds[fundId].currentManager = msg.sender;
		isActiveManager[msg.sender] = true;
	}


	function setPendingManager(uint256 fundId, address pending) public {
		require(funds[fundId].currentManager == msg.sender);
		funds[fundId].pendingManager = pending;
	}


	function claimManagement(uint256 fundId) public {
		require(msg.sender != address(0) && funds[fundId].currentManager != address(0));
		require(funds[fundId].pendingManager == msg.sender);
		require(!isActiveManager[msg.sender]);
		isActiveManager[funds[fundId].currentManager] = false;
		funds[fundId].currentManager = msg.sender;
		funds[fundId].pendingManager = address(0);
		isActiveManager[msg.sender] == true; // A common mistake 
	}

	function getCurrentManager(uint256 fundId) public view returns (address) {
		return funds[fundId].currentManager;
	}

	function getPendingManager(uint256 fundId) public view returns (address) {
		return funds[fundId].pendingManager;
	}
}
