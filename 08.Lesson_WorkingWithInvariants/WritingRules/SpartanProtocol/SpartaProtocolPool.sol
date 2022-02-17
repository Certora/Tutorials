pragma solidity ^0.8.4;

import "./ERC20.sol";

/* 
 * From Spartan Protocol medium post:
 *
 * The Spartan Protocol provides incentives to enable deep capital formation in liquidity pools, 
 * with safe and sustainable creation of synthetic assets.
 *
 * 
 * A simplified explanation of the platform:
 * 
 * This is an implementation of a liquidity pool.
 * A creator of the pool specify 2 tokens to create a liquidity pool.
 * The creator then transfer assets to the pool as he/she wishes and initialize the pool.
 * The product of the amounts of the 2 tokens is being saved.
 * The owner receives 100,000 LP token in exchange for his/her liquidity.
 *
 * Any user can add/remove liquidity to the pool in exchange for LP tokens.
 * 
 *
 */
contract SpartaProtocolPool is ERC20 {
    address token0;
    address token1;
    address owner;

    uint token0Amount;
    uint token1Amount;
    uint K;

    // assigning values on constructor - specifying 2 tokens and the owner is the creator of the pool
    constructor(address _token0, address _token1) {
        token0 = _token0;
        token1 = _token1;
        owner = msg.sender;
    }    
    
    // initializing the pool according to the amount of tokens sent by the creator.
    // the creator receives 100,000 LP tokens (shares) in exchange.
    function init_pool() public {
        require(msg.sender == owner);
        token0Amount = IERC20(token0).balanceOf(address(this));
        token1Amount = IERC20(token1).balanceOf(address(this));
        
        K = token0Amount * token1Amount; 
        balances[owner] = 100000;
        total = balances[owner];
    }

    // adds liquidity to a pool
    function add_liquidity() public returns (uint) {
        // calculate added token0, token1 amounts
        uint added0 = IERC20(token0).balanceOf(address(this)) - token0Amount;
        uint added1 = IERC20(token1).balanceOf(address(this)) - token1Amount;

        // deposit to LP token
        uint units = mint(msg.sender, added0, added1);
        uint LP_total_supply = total;

        K = (K / (LP_total_supply-units)) * (LP_total_supply);
        
        sync();
        return units;
    }

    // removes liqudity from a pool
    function remove_liquidity(uint LP_tokens) public {
        // sync();      // add sync() here to solve the bug
        burn(msg.sender, LP_tokens);
        uint LP_total_supply = total;
        K = K * LP_total_supply / (LP_total_supply + LP_tokens);
    }
    
    // Automated Market Maker (AMM) - calculating the exchange rate of a desired exchange
    function swap(address from_token) public {
        require((from_token == token0 || from_token == token1), "Must be toekn0 or token1");
        address to_token = from_token == token0 ?  token1 : token0;
   
        // get balance for the token_from in user's account and transfer it to the pool
        uint from_token_balance = IERC20(from_token).balanceOf(msg.sender);
        IERC20(from_token).transferFrom(msg.sender, address(this), from_token_balance); // from customer to pool

        // DONT UNDERSTAND
        uint to_token_send = IERC20(from_token).balanceOf(msg.sender) * IERC20(to_token).balanceOf(msg.sender) - K;
        IERC20(to_token).transfer(msg.sender, to_token_send); // From the pool to the customer
        sync();
        
    }

    function getContractAddress() public view returns (address) {
        return address(this);
    }

    function getToken0DepositAddress() public view returns (address) {
        return token0;
    }

    function getToken1DepositAddress() public view returns (address) {
        return token1;
    }

    function sync() public {
        token0Amount = IERC20(token0).balanceOf(address(this));
        token1Amount = IERC20(token1).balanceOf(address(this));
    }
    
    // mints LP tokens to user
    function mint(address user, uint amount0, uint amount1) internal returns (uint){
        uint totalBalance0 = IERC20(token0).balanceOf(address(this));
        uint totalBalance1 = IERC20(token1).balanceOf(address(this));

        // minting deserved from supplying token 0 or 1 is the portion of the user's 
        // supplied liquidity out of the total assets in the pool before the addition.
        uint mint_0 = total * amount0 / (totalBalance0-amount0);
        uint mint_1 = total * amount1 / (totalBalance1-amount1);

        // the liquidity providers are being incentivised to supply liquidity based on the existing ratio.
        // if the user choose to deviate from the ratio, they will get LP tokens according to the lower of the 2 amounts.
        // e.g. if the pool at the moment has 1:3 ratio between ETH and USDC, and the user want to supply lquidity
        // of 3 ETH and 10 USDC, they will receieve 3 LP tokens, as if they supplied 3 ETH and 9 USDC.
        uint to_mint = mint_0 < mint_1 ? mint_0 : mint_1;
        balances[user] += to_mint;
        total += to_mint;
        return to_mint;
    }

    function burn(address user, uint LP_tokens) internal  {
        require(balances[user] >= LP_tokens);
        // calculates the amount of token0 or token1 that the user is eligble to receive.
        // it is the portion of his/her LP tokens out of the total.
        uint pay_in_0 = LP_tokens * IERC20(token0).balanceOf(address(this)) / total;
        uint pay_in_1 = LP_tokens * IERC20(token1).balanceOf(address(this)) / total;
        
        // updates the user's, total, and contract amount of LP token count
        balances[user] -= LP_tokens;
        total -= LP_tokens;
        token0Amount -= pay_in_0;
        token1Amount -= pay_in_1;

        // transfer liquidity token to user
        IERC20(token0).transfer(user, pay_in_0);
        IERC20(token1).transfer(user, pay_in_1);
    }    
    
}