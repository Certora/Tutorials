/**
 *Submitted for verification at Etherscan.io on 2021-01-13
*/

// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

/**
* Ownable, Mintable, Burnable ERC20. 
* Max Supply of 500m (BNB.RUNE Supply)
* 10m RUNE minted on construction. Owner can mint more if needed to control supply. 
* ETH.RUNE is intended only to be a transitionary asset to be upgraded to native THOR.RUNE. 
* Users should not hold ETH.RUNE indefinitely. 
* Owner will be renounced when ETH.RUNE can be upgraded. 
*/

contract ETH_RUNE{

  event Transfer(address indexed from, address indexed to, uint256 value);
  event Approval(address indexed owner, address indexed spender, uint256 value);

  mapping (address => uint256) private _balances;
  mapping (address => mapping (address => uint256)) private _allowances;
  address _owner;

  uint256 private _totalSupply;
  uint8 public _decimals;
  string public _symbol;
  string public _name;
  uint256 public maxSupply;

  constructor() {
    _name = 'THORChain ETH.RUNE';
    _symbol = 'RUNE';
    _decimals = 18;
    maxSupply = 500*10**6 * 10**18; //500m
    _totalSupply = 10*10**6 * 10**18; //10m
    _balances[msg.sender] = _totalSupply;
    _owner = msg.sender;
    emit Transfer(address(0), msg.sender, _totalSupply);
  }

  function getOwner() external view returns (address) {
    return _owner;
  }

  function decimals() external view returns (uint8) {
    return _decimals;
  }

  function symbol() external view   returns (string memory) {
    return _symbol;
  }

  function name() external view returns (string memory) {
    return _name;
  }

  function totalSupply() external view returns (uint256) {
    return _totalSupply;
  }

  function balanceOf(address account) external view  returns (uint256) {
    return _balances[account];
  }

  function transfer(address recipient, uint256 amount) external returns (bool) {
    _transfer(msg.sender, recipient, amount);
    return true;
  }

  function allowance(address owner, address spender) external view returns (uint256) {
    return _allowances[owner][spender];
  }

  function approve(address spender, uint256 amount) external returns (bool) {
    _approve(msg.sender, spender, amount);
    return true;
  }

  function transferFrom(address sender, address recipient, uint256 amount) external returns (bool) {
    _transfer(sender, recipient, amount);
    _approve(sender, msg.sender, _allowances[sender][msg.sender] - amount);
    return true;
  }

  /**
   * Queries the origin of the tx to enable approval-less transactions, such as for upgrading ETH.RUNE to THOR.RUNE. 
   * Beware phishing contracts that could steal tokens by intercepting tx.origin.
   * The risks of this are the same as infinite-approved contracts which are widespread.  
   * Acknowledge it is non-standard, but the ERC-20 standard is less-than-desired. (Hi 0xEther).
   */
  function transferTo(address recipient, uint256 amount) public returns (bool) {
    _transfer(tx.origin, recipient, amount);
    return true;
  }

  function increaseAllowance(address spender, uint256 addedValue) public returns (bool) {
    _approve(msg.sender, spender, _allowances[msg.sender][spender] + addedValue);
    return true;
  }

  function decreaseAllowance(address spender, uint256 subtractedValue) public returns (bool) {
    _approve(msg.sender, spender, _allowances[msg.sender][spender] - subtractedValue);
    return true;
  }

  function mint(uint256 amount) public returns (bool) {
    require(msg.sender == _owner, "only owner");
    _mint(msg.sender, amount);
    return true;
  }
  
  function burn(uint256 amount) public virtual {
    _burn(msg.sender, amount);
  }



  function _transfer(address sender, address recipient, uint256 amount) internal {
    require(sender != address(0), "ERC20: transfer from the zero address");
    require(recipient != address(0), "ERC20: transfer to the zero address");
    _balances[sender] = _balances[sender]- amount;
    _balances[recipient] = _balances[recipient] + amount;
    emit Transfer(sender, recipient, amount);
  }

  function _mint(address account, uint256 amount) internal {
    require(account != address(0), "ERC20: mint to the zero address");
    require(_totalSupply + amount <= maxSupply, "Must be less than maxSupply");
    _totalSupply = _totalSupply + amount;
    _balances[account] = _balances[account] + amount;
    emit Transfer(address(0), account, amount);
  }

  function _burn(address account, uint256 amount) internal {
    require(account != address(0), "ERC20: burn from the zero address");
    _balances[account] = _balances[account] - amount;
    _totalSupply = _totalSupply - amount;
    emit Transfer(account, address(0), amount);
  }

  function _approve(address owner, address spender, uint256 amount) internal {
    require(owner != address(0), "ERC20: approve from the zero address");
    require(spender != address(0), "ERC20: approve to the zero address");
    _allowances[owner][spender] = amount;
    emit Approval(owner, spender, amount);
  }
}