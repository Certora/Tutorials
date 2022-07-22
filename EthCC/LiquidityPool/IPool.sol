interface IPool {
    // Deposit amount of underlying token returning the amount of shares minted to msg.sender   
    function deposit(uint256 amount) external virtual returns(uint256);
    // Withdraw shares and returns the anount of underlying token transfered to msg.sender 
    function withdraw(uint256 shares) external virtual returns (uint256);
    // Flashlaon an amount of underlying token and calls reciverAddress 
    function flashLoan(address receiverAddress, uint256 amount) external virtual ;
}