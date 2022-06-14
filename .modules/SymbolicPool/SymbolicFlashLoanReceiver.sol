import {IPool} from './IPool.sol';
import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
import {IERC20} from './IERC20.sol';

contract SymbolicFlashLoanReceiver is IFlashLoanReceiver {
    IERC20 asset;
    IPool pool;
    uint256 public callBackOption;
    uint256 x;
    address public to;
    address from;

    function executeOperation(uint256 amount,uint256 premium,address initiator) override external returns(bool) {
        if (callBackOption == 0)
        {
            asset.transfer(to,x);
            require(to != address(pool) && to != msg.sender);
        }
        // else if (callBackOption == 2 )
        //     asset.transferFrom(from,to,x);
        else if (callBackOption == 3 )
            pool.deposit(x);
        else if (callBackOption == 4 )
            pool.withdraw(x);
        // else if (callBackOption == 5 )
        //     pool.FlashLoan(to,x);
        return true;
    }
}