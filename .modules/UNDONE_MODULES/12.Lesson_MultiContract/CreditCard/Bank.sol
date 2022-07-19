pragma solidity ^0.8.7;
import "./IBank.sol";
contract Bank is IBank{
    
    mapping (address => uint256) public funds;
    mapping(address => mapping(address => uint256)) allowences;
    uint256 public totalFunds;
    
    function deposit(uint256 amount) public payable {
        require(msg.sender != address(0));
        require(msg.value == amount, "here");
        funds[msg.sender] = funds[msg.sender]+amount;
        totalFunds = totalFunds + amount;
    }
    function getAllowance(address owner, address spender) public view returns (uint256) {
        return allowences[owner][spender];
    }
    
    function transfer(address to, uint256 amount) external {
        require(to!= address(0));
        require(funds[msg.sender] >= amount, "Bank: insufficient funds");
        funds[msg.sender] = funds[msg.sender]-amount;
        funds[to] = funds[to]+amount;
        
    }
    
    function transferFrom(address sender, address receiver, uint256 amount) external {
        uint256 currentAllowance = allowences[sender][msg.sender];
        require(currentAllowance >= amount);
        unchecked {
            _approve(sender, msg.sender, currentAllowance - amount);
        }

        _transfer(sender,receiver, amount);
    }

    function approve(address spender, uint256 amount) external{
        _approve(msg.sender, spender, amount);
    }


    function _transfer(address sender, address reciever, uint256 amount) internal {
        require(sender != address(0));
        require(reciever != address(0));
        uint256 senderBalance = funds[sender];
        require(senderBalance>=amount);
        funds[sender] = senderBalance - amount;
        funds[reciever] += amount;
    }
    function _approve(address owner,address spender, uint256 amount ) internal{
        require(owner != address(0));
        require(spender != address(0));

        allowences[owner][spender] = amount;
    }
    function withdraw(uint256 amount) external payable returns (bool success)  {
        require(amount <= funds[msg.sender]);
        
        funds[msg.sender]-=amount;
        success = payable(msg.sender).send(amount);
        require(success);
        totalFunds = totalFunds-=amount;
    }
    
    function getFunds(address account) external view returns (uint256) {
        return funds[account];
    }
    
    function getTotalFunds() external view returns (uint256) {
        return totalFunds;
    }

    function getEthBalance(address account) external view returns (uint256){
        return account.balance;
    }

    fallback() payable external{}
    receive() payable external{}
}
