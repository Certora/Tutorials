/*
The following system is based on a simplified version of the Trident bug that was found by the certora prover.
Here's a brief explanation about the original system and bug:
https://medium.com/certora/exploiting-an-invariant-break-how-we-found-a-pool-draining-bug-in-sushiswaps-trident-585bd98a4d4f 

*/

pragma solidity ^0.8.0;
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts v4.4.1 (token/ERC20/ERC20.sol)

pragma solidity ^0.8.0;
import "./ERC20.sol";


/*
In constant-product pools liquidity providers (LPs) deposit two types of underlying tokens (Token0 and Token1) in exchange for LP tokens. 
They can later burn LP tokens to reclaim a proportional amount of Token0 and Token1.
Trident users can swap one underlying token for the other by transferring some tokens of one type to the pool and receiving some number of the other token.
To determine the exchange rate, the pool returns enough tokens to ensure that
(reserves0 ⋅ reserves1)ᵖʳᵉ =(reserves0 ⋅ reserves1)ᵖᵒˢᵗ
where reserves0 and reserves1 are the amount of token0, token1 the system holds. 

On first liquidity deposit the system transfers 1000 amount of LP to address 0 to ensure the pool cannot be emptied.  
*/

contract ConstantProductPool is ERC20 {
    uint256 internal constant MINIMUM_LIQUIDTY = 1000;
    address public token0;
    address public token1;
    uint256 internal reserve0;
    uint256 internal reserve1;
    uint256 public kLast;

    uint256 locked;
    modifier lock() {
        require(locked == 1, "LOCKED");
        locked = 2;
        _;
        locked = 1;
    }

    constructor(address _token0, address _token1)  {
        require(token0 != address(0));
        require(token0 != token1);
        token0 = _token0;
        token1 = _token1;
        locked = 1;
    }

    // Mints LP tokens - this is called after an external transfer of token0 and token1
    function mint(address recipent) public lock returns (uint256 liquidity) {
        (uint256 _reserve0, uint256 _reserve1) = _getReserves();
        (uint256 _balance0, uint256 _balance1) = _getBalances();

        uint256 computed = _balance0 * _balance1;
        uint256 amount0 = _balance0 - _reserve0;
        uint256 amount1 = _balance1 - _reserve1;

        uint256 _totalSupply = totalSupply();
        uint256 k = kLast;
        if (_totalSupply == 0) {
            liquidity = MINIMUM_LIQUIDTY - computed;
            require(amount0 > 0 && amount1 > 0, "INVALID AMOUNTS");
            _balances[address(0)] = MINIMUM_LIQUIDTY;
        } else {
            uint256 kIncrease = computed - k;
            liquidity = (kIncrease * _totalSupply) / k;
        }
        require(liquidity != 0, "INSUFFICENT LIQUIDITY");
        _mint(recipent, liquidity);
        kLast = computed;
        _update(_balance0, _balance1);
    }

    // Burns LP tokens and swaps one of the output tokens for another
    // User receives amountOut in tokenOut
    function burnSingle(address tokenOut, uint256 liquidity, address recipent)
        public
        lock
        returns (uint256 amountOut)
    {
        (uint256 _reserve0, uint256 _reserve1) = _getReserves();
        (uint256 balance0, uint256 balance1) = _getBalances();
        uint256 _totalSupply = totalSupply();

        uint256 amount0 = (liquidity * balance0 ) / _totalSupply;
        uint256 amount1 = (liquidity * balance1 ) / _totalSupply;
        
        _burn( recipent, liquidity);
        if (tokenOut == token0) {
            amount1 += _getAmountOut(
                amount0,
                _reserve0 - amount0,
                _reserve1 - amount1
            );
            transfer(recipent,token1, amount1);
            balance1 -= amount1;
            amountOut = amount1;
            amount0 = 0;
        } else {
            require(tokenOut == token1, "INVALID TOKEN");
            amount0 += _getAmountOut(
                amount1,
                _reserve1 - amount1,
                _reserve0 - amount0
            );
            transfer(recipent, token0, amount0);
            balance0 -= amount0;
            amountOut = amount0;
            amount1 = 0;
        }
        _update(balance0, balance1);
    }

    // Swaps one token for another
    function swap(address tokenIn, address recipient)
        public
        lock
        returns (uint256 amountOut)
    {
        (uint256 _reserve0, uint256 _reserve1) = _getReserves();
        (uint256 balance0, uint256 balance1) = _getBalances();
        require(_reserve0 > 0);
        uint256 amountIn;
        address tokenOut;
        if (tokenIn == token0) {
            tokenOut = token1;
            amountIn = balance0 - _reserve0;
            amountOut = _getAmountOut(amountIn, _reserve0, _reserve1);
            balance1 -= amountOut;
        } else {
            require(tokenIn == token1, "INVALID TOKEN");
            tokenOut = token0;
            amountIn = balance1 - _reserve1;
            amountOut = _getAmountOut(amountIn, _reserve1, _reserve0);
            balance0 -= amountOut;
        }
        transfer(tokenOut, recipient, amountOut);
        _update(balance0, balance1);
    }

    function transfer(
        address to,
        address token,
        uint256 amount
    ) internal {
        bool success = ERC20(token).transferFrom(address(this), to, amount);
        require(success, "TRANSFER FAILED");
    }

    function _update(
        uint256 balance0,
        uint256 balance1
    ) internal {
        reserve0 = balance0;
        reserve1 = balance1;
    }

    function getReserve0() public view returns (uint256) {
        return reserve0;
    }

    function getReserve1() public view returns (uint256) {
        return reserve1;
    }

    function _getAmountOut(
        uint256 amountIn,
        uint256 reserveAmountIn,
        uint256 reserveAmountOut
    ) internal pure returns (uint256 amountOut) {
        amountOut =
            (amountIn * reserveAmountOut) /
            (reserveAmountIn + amountIn);
    }

    function _getReserves()
        internal
        view
        returns (uint256 _reserve0, uint256 _reserve1)
    {
        _reserve0 = reserve0;
        _reserve1 = reserve1;
    }

    function _getBalances()
        internal
        view
        returns (uint256 _balance0, uint256 _balance1)
    {
        _balance0 = ERC20(token0).balanceOf(address(this));
        _balance1 = ERC20(token1).balanceOf(address(this));
    }
}
