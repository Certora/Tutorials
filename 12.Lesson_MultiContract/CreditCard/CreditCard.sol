pragma solidity ^0.8.7;
import "./Bank.sol";


contract CreditCard{

    mapping(uint256 => Bank) banks;
    uint256 feeRate;
    uint256 feePrecision;
    address owner;
    constructor(uint256 rate, uint256 _feePrecision){
        owner = msg.sender;
        feeRate = rate;
        feePrecision = _feePrecision;
    }

    function pay(Bank senderBank, Bank recipientBank, address recipient, uint256 amount) public {
        require(senderBank.getAllowance(msg.sender,address(this))>=amount, "Please allow the credit to transfer the funds");
        uint256 fee = calculateFee(amount);
        uint256 updatedAmount = fee + amount;
        senderBank.transferFrom(msg.sender, address(this), updatedAmount);
        senderBank.withdraw(updatedAmount);
        //(bool success, bytes memory data) = payable(address(recipientBank)).call{value: updatedAmount}(abi.encodeWithSignature("deposit(uint256)", updatedAmount));
        recipientBank.deposit{value:updatedAmount}(updatedAmount);
        recipientBank.transfer(recipient, updatedAmount);
    }
    ///property: pay twice, each time with amount/2< pay once with amount
    function calculateFee(uint256 amount) view public returns (uint256){
        uint256 fee = amount * feeRate ** feeRate / feePrecision;
        return fee;
    }
    function getRate() view public returns (uint256) {
        return feeRate;
    }
    fallback() external payable{}
    receive() external payable{}
}