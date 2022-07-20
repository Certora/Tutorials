// SPDX-License-Identifier: agpl-3.0


/**

 This example is based on a cirtical bug found by Certora Prover in KashiPair while on development.
 The bug can cause a loss of system's assets during liquidation.
 More information is in the verification report https://www.certora.com/pubs/KashiLendingMar2021.pdf and in this talk https://www.youtube.com/watch?v=VGSsPIsbb6U 


***/
pragma solidity ^0.8.0;

interface IERC20 {
	function transfer(address to, uint value) external;
	function transferFrom(address from, address to, uint value) external;
}

interface IOracle {
	function get(IERC20 token1, IERC20 token2) external returns (uint256);
}

contract BorrowSystemBroken {
	// oracle to be used
	IOracle oracle;
	// ERC20 collateralToken
	IERC20 public collateralToken;
	// ERC20 borrowToken 
	IERC20 public borrowToken;

	// amount of borrowToken user borrowed
	mapping(address => uint256) public userBorrowAmount;
	// amount of collateralToken user has deposited
	mapping(address => uint256) public userCollateralAmount;

	/* 
	 * Check if a user's collateral balance covers his borrow according
	 * to the current price. Returns true when the user is solvent.
	 */
	function _isSolvent(address user) private returns (bool) {
		uint256 rate = oracle.get(borrowToken, collateralToken);

		require(rate != 0);

		return userBorrowAmount[user] == 0 || userBorrowAmount[user] * rate < userCollateralAmount[user];
	}
	
	/* Borrow amount and provide collateral */
	function borrow(uint256 borrowAmount, uint256 collateralAmount) public {
		userBorrowAmount[msg.sender] = borrowAmount;
		userCollateralAmount[msg.sender] = collateralAmount;

		require(_isSolvent(msg.sender), "user is not solvent");

		borrowToken.transfer(msg.sender, borrowAmount);
		collateralToken.transferFrom(msg.sender, address(this), collateralAmount);
	}

	/* The user (msg.sender) repays a part of its borrow and gets back a part of his collateral */
	function repay(uint256 borrowAmount, uint256 collateralAmount) public {
		
		require(_isSolvent(msg.sender), "user is not solvent");
		
		userBorrowAmount[msg.sender] -= borrowAmount;
		userCollateralAmount[msg.sender] -= collateralAmount;


		borrowToken.transferFrom(msg.sender, address(this), borrowAmount); 
		collateralToken.transfer(msg.sender, collateralAmount);
	}

	/* 
	 * Liquidation of a user that is in insolvent state.
	 *     user - address to liquidate
	 *     to - address to receive collateral
	 */ 
	function liquidate(address user, address to) public {
		require(!_isSolvent(user), "user is solvent");

		uint256 borrow = userBorrowAmount[user];
		uint256 collateral = userCollateralAmount[user];

		userBorrowAmount[user] = 0;
		userCollateralAmount[user] = 0;

		// msg.sender gives borrowToken to the system and this contract
		// sends collateralToken to 'to'
		borrowToken.transferFrom(msg.sender, address(this), borrow);
		collateralToken.transfer(to, collateral); 
	}

	// actions for the batchCalls
	uint8 internal constant CALL_BORROW = 1;
	uint8 internal constant CALL_REPAY = 2;

	/*
	 * Allows calling a few functions in a batch mode and interaction 
	 * with other contracts.
	 */
	function batchCalls(
		uint8[] calldata actions,
		uint256[] calldata borrowAmount,
		uint256[] calldata collateralAmount,
		address[] calldata callee,
		bytes[] calldata datas
	) external {
		for (uint256 i = 0; i < actions.length; i++) {
			uint8 action = actions[i];

			if (action == CALL_BORROW) {
				borrow(borrowAmount[i], collateralAmount[i]);
			} else if (action == CALL_REPAY) {
				repay(borrowAmount[i], collateralAmount[i]);
			} else {
				require(callee[i] != address(collateralToken) && 
						callee[i] != address(borrowToken));
				callee[i].call(datas[i]);
			}
		}
	}
}