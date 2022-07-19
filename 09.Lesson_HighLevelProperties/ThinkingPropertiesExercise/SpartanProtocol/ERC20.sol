pragma solidity ^0.8.4;


interface IERC20 {
    function myAddress() external  returns (address);
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function getAllowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function increase_allowance(address to_user, uint inc_amount) external;
    function decrease_allowance(address from_user, uint dec_amount) external;
}

contract ERC20 is IERC20 {
    uint256 total;
    mapping (address => uint) balances;
    mapping (address => mapping (address => uint)) allowance;

    string public name;
    string public symbol;
    uint public decimals;

    function myAddress() external override returns (address) {
        return address(this);
    }

    function totalSupply() external view override returns (uint256) {
        return total;
    }

    function balanceOf(address account) external override view returns (uint256) {
        return balances[account];
    }

    function transfer(address recipient, uint256 amount) external override returns (bool) {
        balances[msg.sender] -= amount;
        balances[recipient] += amount;
        return true;
    }

    function getAllowance(address owner, address spender) external view override returns (uint256) {
        return allowance[owner][spender];
    }

    function approve(address spender, uint256 amount) external override returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) external override returns (bool) {
        balances[sender] -= amount;
        balances[recipient] += amount;
        allowance[sender][msg.sender] -=  amount;
     
        return true;
    }

    function increase_allowance(address to_user, uint inc_amount) external override {
        require(allowance[msg.sender][msg.sender] >= inc_amount);
        allowance[msg.sender][msg.sender] -= inc_amount;
        allowance[msg.sender][to_user] += inc_amount;
    }

    function decrease_allowance(address from_user, uint dec_amount) external override {
        require(allowance[msg.sender][from_user] >= dec_amount);
        allowance[msg.sender][from_user] -= dec_amount;
        allowance[msg.sender][msg.sender] += dec_amount;
    }

}