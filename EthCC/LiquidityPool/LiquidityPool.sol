import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
import {ERC20} from './ERC20.sol';
import {IERC20} from './IERC20.sol';
import {IPool} from './IPool.sol';
pragma solidity >=0.8.0;

/* 

This is a simplified liquidity pool

This liquidity pool is for a single ERC20 token and collects fees from flashloans. Fees are distributed to liquidity holders according to shares. 
The liquidity pool is an ERC20 token by iteslf, it mints token on deposits and burn them to withdraw the undelying asset. 

The main functions here are:

  1) deposit(uint256 amount)   
  For depositing amount of underlying. return value is the amount of shares the user recieved for his deposits. 
.
  2) withdraw(uint256 shares)
  For withdrawing shares and receiving back underlying token.

  3) flashLoan(uint256 amount) 
  A loan one can take, perform some action, and pay back to the system with fee.
  

*/

contract LiquidityPool is ERC20, IPool {

   uint256 private constant _NOT_ENTERED = 1;
  uint256 private constant _ENTERED = 2;

  uint256 private _status;
  modifier nonReentrant() {
        // On the first call to nonReentrant, _notEntered will be true
        require(_status != _ENTERED, "ReentrancyGuard: reentrant call");

        // Any calls to nonReentrant after this point will fail
        _status = _ENTERED;

        _;

        // By storing the original value once again, a refund is triggered (see
        // https://eips.ethereum.org/EIPS/eip-2200)
        _status = _NOT_ENTERED;
    }

  IERC20 public asset;   
  uint256 private constant feePrecision = 10000; 
  //feeRate is up to 1%, so less than 100 as it is divided by feePrecision
  uint256 public feeRate; 

  function sharesToAmount(uint256 shares) public view  returns (uint256) {
     uint256 poolBalance=asset.balanceOf(address(this));  
     return shares * poolBalance / totalSupply();  
  }


  function amountToShares(uint256 amount) public view  returns (uint256) {
      uint256 poolBalance=asset.balanceOf(address(this));   
      return amount * totalSupply() / poolBalance;   
  }

  function deposit(uint256 amount) external override nonReentrant() returns(uint256 shares) {
      uint256 poolBalance=asset.balanceOf(address(this));
        if (totalSupply()==0 || poolBalance == 0){
            shares = amount;
        }
        else{
          shares = amountToShares(amount);
          require (shares != 0);
        }
        asset.transferFrom(msg.sender,address(this),amount);
        _mint(msg.sender,shares);
    }


  function withdraw(uint256 shares) external override nonReentrant() returns (uint256 amountOut)  {
    uint256 poolBalance = asset.balanceOf(address(this));
    require (poolBalance != 0);
    amountOut = sharesToAmount(shares);
    require (amountOut != 0);
   	_burn(msg.sender,shares);
		asset.transferFrom(address(this),msg.sender,amountOut);
    }

    
  function flashLoan(address receiverAddress, uint256 amount) nonReentrant() external override {          
    uint256 totalPremium = calcPremium(amount);
    require (totalPremium != 0);
    uint256 amountPlusPremium = amount + totalPremium;
    asset.transferFrom(address(this),msg.sender,amount);
    require(IFlashLoanReceiver(receiverAddress).executeOperation(amount,totalPremium,msg.sender),'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
    asset.transferFrom(msg.sender,address(this),amountPlusPremium);
  }

  function calcPremium(uint256 amount) public returns (uint256){
    return ((amount*feeRate)/feePrecision);
  }

}
