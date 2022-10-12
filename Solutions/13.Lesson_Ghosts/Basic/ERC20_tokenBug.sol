contract ERC20_tokenBug {
    mapping (address => uint256) balances;
    uint256 totalSupply;

    function getTotalSupply() public view returns(uint256)
    {
        return totalSupply;
    }
    function getBalance(address user) public view returns(uint256){
        return balances[user];
    }

    function transfer(address to, uint256 amount) public{
        unchecked {
            balances[msg.sender] -= amount;
            balances[to] += amount;
        }
        
    }

    function mint(address to, uint256 amount) public {
        totalSupply += amount;
        balances[to] += amount;
    }

    function burn(address to, uint256 amount) public {
        totalSupply -= amount;
        balances[to] -= amount;
    }
}