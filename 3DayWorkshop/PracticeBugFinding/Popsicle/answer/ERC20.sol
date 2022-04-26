// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.4;

// with mint
contract ERC20 {
    uint256 total;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowance;

    string public name;
    string public symbol;
    uint public decimals;



    function totalSupply() external view returns (uint256) {
        return total;
    }
    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }
    function transfer(address recipient, uint256 amount) virtual external returns (bool) {
        balances[msg.sender] -= amount;
        balances[recipient] += amount;
        return true;
    }
    function allowanceOf(address owner, address spender) external view returns (uint256) {
        return allowance[owner][spender];
    }
    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }
    function transferFrom(address sender, address recipient, uint256 amount) virtual external returns (bool) {
        balances[sender] -=  amount;
        balances[recipient] += amount;
        allowance[sender][msg.sender] -=  amount;
        return true;
    }



    function mint(address user, uint amount) internal {
        /* 
            user - assign the minted shares to user.
            amount - number of shares to mint.
        */
        total += amount;
        balances[user] += amount;        
    }

    function burn(address user, uint amount) internal {
        /* 
            user - burn the shares from user.
            amount - number of shares to burn.
        */
        
        balances[user] -= amount;        
        total -= amount;
        
    }


    
}