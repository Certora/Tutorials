// SPDX-License-Identifier: agpl-3.0

pragma solidity ^0.8.4;

contract ERC20 {
    uint256 total;
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowance;

    string public name;
    string public symbol;
    uint public decimals;

    function myAddress() public returns (address) {
        return address(this);
    }

    function add(uint a, uint b) internal pure returns (uint256) {
        uint c = a +b;
        require (c >= a);

        return c;
    }

    function sub(uint a, uint b) internal pure returns (uint256) {
        require (a>=b);

        return a-b;
    }

    function totalSupply() external view returns (uint256) {
        return total;
    }

    function balanceOf(address account) external view returns (uint256) {
        return balances[account];
    }

    function transfer(address recipient, uint256 amount) external returns (bool) {
        balances[msg.sender] = sub(balances[msg.sender], amount);
        balances[recipient] = add(balances[recipient], amount);

        return true;
    }

    function allowanceOf(address owner, address spender) external view returns (uint256) {
        return allowance[owner][spender];
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;

        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool) {
        balances[sender] = sub(balances[sender], amount);
        balances[recipient] = add(balances[recipient], amount);
        allowance[sender][msg.sender] = sub(allowance[sender][msg.sender], amount);

        return true;
    }   

    function increase_allowance(address to_user, uint inc_amount) external {
        require(allowance[msg.sender][msg.sender] >= inc_amount);
        allowance[msg.sender][msg.sender] -= inc_amount;
        allowance[msg.sender][to_user] += inc_amount;
    }

    
    function decrease_allowance(address from_user, uint dec_amount) external {
        require(allowance[msg.sender][from_user] >= dec_amount);
        allowance[msg.sender][from_user] -= dec_amount;
        allowance[msg.sender][msg.sender] += dec_amount;
    }

    /*
     * 
     */
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
        msg.sender.call{value: amount}("");
    }

}