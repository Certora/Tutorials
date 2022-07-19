pragma solidity ^0.8.4;
import "./ERC20.sol";

/* Example based on Popsicle Finance Sorbetto Fragola  


 * This contract acts as a liquidity pool and gaines fees for the benefit 
 * of the investor.
 * 
 */

contract PopsicleFinance is ERC20 {
    event Deposit(address user_address, uint deposit_amount);
    event Withdraw(address user_address, uint withdraw_amount);
    event CollectFees(address collector, uint totalCollected);
    
    
    address owner;
    uint totalFeesEarnedPerShare = 0; // total fees earned per share

    mapping (address => UserInfo) accounts;
    
    constructor() {
        owner = msg.sender;
    }
    
    struct UserInfo {
        uint feesCollectedPerShare; // the total fees per share that have been already collected
        uint Rewards; // general "debt" of popsicle to the user 
    }

    // deposit assets (ETH) to the system in exchange for shares
    function deposit() public payable {
        uint amount = msg.value;
        // reward is set to be the amount of fees that have accumulated, but yet to be collected. (total, not per share)
        uint reward = balances[msg.sender] * (totalFeesEarnedPerShare - accounts[msg.sender].feesCollectedPerShare);
        // once the reward has been saved, the collected fees are updated
        accounts[msg.sender].feesCollectedPerShare = totalFeesEarnedPerShare;
        accounts[msg.sender].Rewards += reward;
        // Popsicle are minting "share tokens" owed to the user
        mint(msg.sender, amount);
        emit Deposit(msg.sender, amount);
    }

    // withdraw assets (shares) from the system
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        // reward is set to be the amount of fees that have been accumulated, but yet to be collected. (total, not per share)
        uint reward = amount * (totalFeesEarnedPerShare - accounts[msg.sender].feesCollectedPerShare);
        // Popsicle are burning "share tokens" owed by the user
        burn(msg.sender, amount);
        // updating the user's deserved rewards count
        accounts[msg.sender].Rewards += reward;
        emit Withdraw(msg.sender, amount);
    }

    // collect fees
    function collectFees() public {
        require(totalFeesEarnedPerShare >= accounts[msg.sender].feesCollectedPerShare);
        // the amount of fees (rewards) per share that have yet to be collected.
        uint fee_per_share = totalFeesEarnedPerShare - accounts[msg.sender].feesCollectedPerShare;
        // the already counted rewards + the rewards that haven't been 
        uint to_pay = fee_per_share * balances[msg.sender] + accounts[msg.sender].Rewards;
        // updating the indicator of collected fees
        accounts[msg.sender].feesCollectedPerShare = totalFeesEarnedPerShare;
        // nullifying user's deserved rewards
        accounts[msg.sender].Rewards = 0;
        // paying the user
        msg.sender.call{value: to_pay}("");
        emit CollectFees(msg.sender, to_pay);
    }
    
    function OwnerDoItsJobAndEarnsFeesToItsClients() public payable {
        totalFeesEarnedPerShare += 1;
    }

    // added by Certora for use in a spec - returns the deserved rewards collected up to this point.
    function assetsOf(address user) public view returns(uint) {
        return accounts[user].Rewards + balances[user] * (totalFeesEarnedPerShare - accounts[user].feesCollectedPerShare);
    }
}
