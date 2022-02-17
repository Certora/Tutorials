import {IFlashLoanReceiver} from './IFlashLoanReceiver.sol';
import {ERC20} from './ERC20.sol';
import {IERC20} from './IERC20.sol';
pragma solidity >=0.8.0;


contract Pool is ERC20 {

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

    function sharesToAmount(uint256 shares) public view returns (uint256) {
        uint256 poolBalance = asset.balanceOf(address(this)); 
        return shares * poolBalance / totalSupply();
    }

    function amountToShares(uint256 amount) public view returns (uint256) {
        uint256 poolBalance = asset.balanceOf(address(this));   
        return amount * totalSupply() / poolBalance;
    }

    function deposit(uint256 amount) public payable nonReentrant() returns(uint256 shares) {
        uint256 poolBalance = asset.balanceOf(address(this));
        if (totalSupply() == 0 || poolBalance == 0){
            shares = amount; 
        }
        else{
            shares = amountToShares(amount);
            require (shares != 0);
        }
        asset.transferFrom(msg.sender, address(this), amount);
        _mint(msg.sender, shares);
    }

    function withdraw(uint256 shares) public nonReentrant() returns (uint256 amountOut)  {
        amountOut = sharesToAmount(shares);
        require (amountOut != 0);
        _burn(msg.sender, shares);
		asset.transferFrom(address(this), msg.sender, amountOut);
    }

    function flashLoan(address receiverAddress, uint256 amount) nonReentrant() public {          
        uint256 totalPremium = calcPremium(amount);
        require (totalPremium != 0);
        uint256 amountPlusPremium = amount + totalPremium;
        asset.transferFrom(address(this), msg.sender, amount);
        require(IFlashLoanReceiver(receiverAddress).executeOperation(amount, totalPremium, msg.sender), 'P_INVALID_FLASH_LOAN_EXECUTOR_RETURN');
        asset.transferFrom(msg.sender, address(this), amountPlusPremium);
        // @note what promises that sender has enough money to return to the pool?
    }

    function calcPremium(uint256 amount) public returns (uint256){
        return ((amount*feeRate)/feePrecision);
    }
}
