pragma solidity ^0.5.0;
/*
This example is based on a real bug from test version of the Maker MCD system 
see https://www.certora.com/blog/why-testing-is-not-enough-for-million-dollar-code.html
*/

contract TokenInterface {
	function mint(address who, uint amount) internal;
	function transferTo(address _to, uint256 _value) public returns (bool success);
	function getTotalSupply() public view returns (uint256);
}

library SafeMath {
	function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");
        return c;
    }

	function safeSub(uint256 x, uint256 y) internal pure returns (uint256) {
		assert(x >= y);
		uint256 z = x - y;
		return z;
    }
}

contract Token is TokenInterface {
	using SafeMath for uint256;
	
    mapping (address => uint) balances;
    uint public totalSupply;
	
	function mint(address who, uint amount) internal  {
		balances[who] = balances[who].safeAdd(amount);
		totalSupply = totalSupply.safeAdd(amount);
	}
  
	function transferTo(address _to, uint256 _value) public returns (bool success) {
		if (balances[msg.sender] >= _value && _value > 0) {
			balances[_to] = balances[_to].safeAdd(_value);
			balances[msg.sender] = balances[msg.sender].safeSub(_value);
			return true;
		} else {
			return false;
		}
    }
    
    function balanceOf(address _owner) public view returns (uint) {
        return balances[_owner];
    }
	
	function getTotalSupply() public view returns (uint) {
		return totalSupply;
	}
}

contract AuctionImpl is TokenInterface {
/*
	Implementation of a reverse auction where bidders offer to take decreasing prize amounts for a fixed payment.
	The bidder who has offered to take the lowest prize value is the winner.
	The auction terminates after a fixed amount of time, or if no one submits a new winning bid for one hour.
	Upon termination, the system mints an amount of tokens equal to the winning bid’s prize value, and transfers it to the winner.

*/
	using SafeMath for uint256;
	
	address public owner ;
	modifier authorized { require(msg.sender == owner); _; }
	
	struct AuctionStrcut {
		uint prize; // the prize decreasing by every bid
		uint payment; // the payment to be paid by the last winner
		address winner; //the current winner
		uint bid_expiry; 	
		uint end_time; 
	}
	
	mapping (uint => AuctionStrcut) auctions;
	
	function getAuction(uint id) public view returns (uint,uint,address,uint,uint) {
		return (auctions[id].prize, auctions[id].payment, auctions[id].winner,auctions[id].bid_expiry, auctions[id].end_time);
	}
		
	function newAuction(uint id, uint payment) public authorized {
		require(auctions[id].end_time == 0); //check id in not occupied
		auctions[id] = AuctionStrcut(2**256-1,payment,owner, 0, now+1 days);
                         // arguments: prize, payment, winner, bid_expiry, end_time
	}
    
	function bid(uint id, uint b) public {
		require(b < auctions[id].prize); // prize can only decrease
		// new winner pays by repaying last winner
		require(transferTo(auctions[id].winner, auctions[id].payment));

		// update new winner with new prize
		auctions[id].prize = b;
		auctions[id].winner = msg.sender;
		auctions[id].bid_expiry = now + 1 hours;
	}
  
	function close(uint id)  public {
		require(auctions[id].bid_expiry != 0
				&& (auctions[id].bid_expiry < now || 
					auctions[id].end_time < now));
		mint(auctions[id].winner, auctions[id].prize);
		delete auctions[id];
	}
  
}

contract System is Token, AuctionImpl {

}

