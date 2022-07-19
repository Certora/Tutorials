pragma solidity ^0.7.0;

library SafeMath {
    function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

    function safeSub(uint256 x, uint256 y) internal pure returns(uint256) {
		assert(x >= y);
		uint256 z = x - y;
		return z;
    }
}

contract Bank {
	using SafeMath for uint256;
	
	mapping (address => uint256) private funds;
	uint256 private totalFunds;
	
	function deposit(uint256 amount) public payable {
		require(msg.sender != address(0));
		funds[msg.sender] = funds[msg.sender].safeAdd(amount);
		totalFunds = totalFunds.safeAdd(amount);
	}
	
	function transfer(address to, uint256 amount) public {
		require(to!= address(0));
		require(funds[msg.sender] > amount);
		funds[msg.sender] = funds[msg.sender].safeSub(amount);
		funds[to] = funds[to].safeAdd(amount);
		
	}
	
	function withdraw() public returns (bool success)  {
		uint256 amount = getFunds(msg.sender);
		funds[msg.sender] = 0;
		success = msg.sender.send(amount);
		require(success);
		totalFunds = totalFunds.safeSub(amount);
	}
	
	function getFunds(address account) public view returns (uint256) {
		return funds[account];
	}
	
	function getTotalFunds() public view returns (uint256) {
		return totalFunds;
	}

	function getEthBalance(address account) public view returns (uint256){
		return account.balance;
	}
}
