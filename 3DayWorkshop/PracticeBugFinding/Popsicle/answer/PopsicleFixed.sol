pragma solidity ^0.8.4;


/**

 This example is based on a bug in Popsicle Finance which was exploited by an attacker in August 2021. https://twitter.com/PopsicleFinance/status/1422748604524019713?s=20.  The attacker managed to drain approximately $20.7 million in tokens from the project’s Sorbetto Fragola pool.

***/


import {ERC20} from './ERC20.sol';
import {Receiver} from '../Receiver.sol';

/* 
    The popsicle finance platform is used by pools liquidity providers to maximize their fees gain from providing liquidity to pools. 
*/


contract PopsicleFixed is ERC20 {
    event Deposit(address user_address, uint deposit_amount);
    event Withdraw(address user_address, uint withdraw_amount);
    event CollectFees(address collector, uint totalCollected);
    
    
    address owner;
    uint public currentUpdate = 1; // total fees earned per share

    mapping (address => UserInfo) public accounts;
    
    constructor() {
        owner = msg.sender;
    }
    
    struct UserInfo {
        uint latestUpdate; 
        uint rewards; // general "debt" of popsicle to the user 
    }

    modifier updateVault(address user) {
        uint reward = balances[user] * (currentUpdate - accounts[user].latestUpdate);
        accounts[user].latestUpdate = currentUpdate;
        accounts[user].rewards += reward;
        _;
    }

    function deposit() public payable {
        uint amount = msg.value;
        uint reward = balances[msg.sender] * (currentUpdate - accounts[msg.sender].latestUpdate);
        accounts[msg.sender].latestUpdate = currentUpdate;
        accounts[msg.sender].rewards += reward;
        mint(msg.sender, amount);
        emit Deposit(msg.sender, amount);
    }


    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        uint reward = amount * (currentUpdate - accounts[msg.sender].latestUpdate);
        burn(msg.sender, amount);
        accounts[msg.sender].latestUpdate = currentUpdate;
        accounts[msg.sender].rewards += reward;
        Receiver(payable(msg.sender)).acceptEth{value: amount}();
        emit Withdraw(msg.sender, amount);
    }

    function collectFees() public {
        require(currentUpdate >= accounts[msg.sender].latestUpdate);
        uint fee_per_share = currentUpdate - accounts[msg.sender].latestUpdate;  
        uint to_pay = fee_per_share * balances[msg.sender] + accounts[msg.sender].rewards;
        accounts[msg.sender].latestUpdate = currentUpdate;
        accounts[msg.sender].rewards = 0;
        Receiver(payable(msg.sender)).acceptEth{value: to_pay}();
        emit CollectFees(msg.sender, to_pay);
    }
    
    function OwnerDoItsJobAndEarnsFeesToItsClients() public payable {
        currentUpdate += 1;
    }

    function transfer(address recipient, uint amount) public override returns(bool) {
        return transferFrom(msg.sender, recipient, amount);
    }

    function transferFrom(address sender, address recipient, uint amount) 
             updateVault(sender) updateVault(recipient) public override returns(bool) {
        require(balances[sender] >= amount);
        balances[sender] = balances[sender] - amount;
        balances[recipient] = balances[recipient] + amount;
        return true;
    }
    // ----------------------------------------------------------------------------------

    // added for spec
    function currentBalance(address user) public view returns(uint) {
        return accounts[user].rewards + balances[user] * (currentUpdate - accounts[user].latestUpdate);
    }

    function ethBalance(address user) public view returns(uint) {
        return user.balance;
    }
}
