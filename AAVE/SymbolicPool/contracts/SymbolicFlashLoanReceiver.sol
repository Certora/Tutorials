// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;
import {IPool} from '../interfaces/IPool.sol';
import {IFlashLoanReceiver} from '../interfaces/IFlashLoanReceiver.sol';
import {IERC20} from '../interfaces/IERC20.sol';

contract SymbolicFlashLoanReceiver is IFlashLoanReceiver {
    IERC20 asset;
    IPool pool;
    uint256 public callBackOption;
    uint256 x;
    address public to;
    address from;
    function executeOperation(uint256 amount,uint256 premium,address initiator) 
    override external returns(bool) {
        if (callBackOption == 0) {
            asset.transfer(to,x);
            require(to != address(pool) && to != msg.sender);
        }
        else if (callBackOption == 1 )
            pool.deposit(x);
        else if (callBackOption == 2 )
            pool.withdraw(x);
        return true;
    }
}