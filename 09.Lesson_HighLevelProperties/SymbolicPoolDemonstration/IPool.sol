interface IPool {
    function deposit(uint256 amount) external payable returns(uint256);
    function withdraw(uint256 shares) external returns (uint256);
    function FlashLoan(address receiverAddress, uint256 amount) external ;
}