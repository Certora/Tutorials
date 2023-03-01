// SPDX-License-Identifier: agpl-3.0
pragma solidity ^0.8.13;


// With approval checks
contract DummyERC20Impl {

    uint256 private _totalSupply;
    mapping (address => uint256) private balances;
    mapping (address => mapping (address => uint256)) private _allowance;

    string public name;
    string public symbol;
    uint public decimals;


    /*-----------------------------------------------
    |                   getters                     |
    -----------------------------------------------*/

    function myAddress() public returns (address) {
        return address(this);
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowance[owner][spender];
    }


    /*-----------------------------------------------
    |                  operations                   |
    -----------------------------------------------*/

    function transfer(address recipient, uint256 amount) external returns (bool) {
        require(msg.sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");

        balances[msg.sender] -= amount;
        balances[recipient] += amount;
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowance[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint256 amount
    ) external returns (bool) {
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(sender != address(0), "ERC20: transfer from the zero address");

        return _transferFrom(sender, recipient, amount);
    }

    function _transferFrom(address sender, address recipient, uint256 amount) internal returns (bool) {
        balances[sender] -= amount;
        balances[recipient] += amount;

        // Update _allowance
        if (sender != msg.sender) {
            _allowance[sender][msg.sender] -= amount;
        }

        return true;
    }
}
