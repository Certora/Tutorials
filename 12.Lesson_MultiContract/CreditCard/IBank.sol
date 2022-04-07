interface IBank {
    function deposit(uint256) external payable;
    function getAllowance(address owner, address spender) view external returns (uint256 allowance);
    function transfer(address to, uint256 amount) external;
    function transferFrom(address sender, address receiver, uint256) external;
    function approve(address spender, uint256 amount) external;
    function withdraw(uint256 amount) external payable returns (bool success);
    function getFunds(address account) external view returns (uint256);
    function getTotalFunds() external view returns (uint256);
    function getEthBalance(address account) external view returns (uint256);
}