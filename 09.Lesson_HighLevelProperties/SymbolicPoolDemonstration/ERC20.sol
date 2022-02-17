pragma solidity >=0.8.0;

import "./IERC20.sol";

abstract contract ERC20  is IERC20{

    uint256 private _totalSupply;
    mapping(address => uint256) private _balanceOf;
    mapping(address => mapping(address => uint256)) private _allowance;

    function totalSupply() public view override returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view override returns (uint256) {
        return _balanceOf[account];
    }

    function allowance(address owner, address spender) public view virtual override returns (uint256)
    {
        return _allowance[owner][spender];
    }

    function approve(address spender, uint256 amount) override external returns (bool) {
        _allowance[msg.sender][spender] = amount;
     
        return true;
    }

    function transfer(address recipient, uint256 amount) override external returns (bool) {
        _balanceOf[msg.sender] -= amount;
        _balanceOf[recipient] += amount;
        
        return true;
    }

    function transferFrom(address from,address recipient,uint256 amount) override external returns (bool) {
        if (_allowance[from][msg.sender] != type(uint256).max) 
        {
            _allowance[from][msg.sender] -= amount;
        }
        _balanceOf[from] -= amount;
        _balanceOf[recipient] += amount;

        return true;
    }

    function _mint(address recipient, uint256 amount) internal {
        _totalSupply += amount;
        _balanceOf[recipient] += amount;
    }

    function _burn(address user, uint256 amount) internal {
        _totalSupply -= amount;
        _balanceOf[user] -= amount;
    }
     
}