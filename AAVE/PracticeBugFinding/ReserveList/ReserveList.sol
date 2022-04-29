pragma solidity ^0.8.7;

import "./IReserveList.sol";

/* 
 * A contract that mimics the AAVE data structure.
 * The concept of two dependent data structures, in our case reserves that pairs tokens with reserves,
 * and underlyingList that pairs tokens with unique ids.
 * @note that the id in each reserve should correlate with the index of the token used as the key in underlyingList.
 *
 */
 
contract ReserveList is IReserveList {
    mapping(address => ReserveData) internal reserves;
    mapping(uint256 => address) internal underlyingList;
    uint16 internal reserveCount = 1;

    function getTokenAtIndex(uint256 index) external view override returns (address) {
        return underlyingList[index];
    }

    function getIdOfToken(address token) external view override returns (uint256) {
        return reserves[token].id;
    }

    function getReserveCount() external view override returns (uint256) {
        return reserveCount;
    }

    function addReserve(address token, address stableToken, address varToken,  uint256 fee) external override {
        bool alreadyAdded = reserves[token].id != 0 || underlyingList[0] == token;
        require(!alreadyAdded, "reserve is already in the database");
        reserves[token] = ReserveData({
            id: 0, 
            lpToken: token, 
            stableDebtToken: stableToken,
            varDebtToken: varToken,
            fee: fee
            });
        
        // A loop designated to fill holes in the list.
        for (uint16 i = 1; i < reserveCount; i++) {
            if (underlyingList[i] == address(0)) {
                reserves[token].id = i;
                underlyingList[i] = token;
            }
        }
        reserves[token].id = reserveCount;
        underlyingList[reserveCount] = token;
        reserveCount = reserveCount + 1;
    }

    function removeReserve(address token) external override {
        underlyingList[reserves[token].id] = address(0);
        delete reserves[token];
        reserveCount = reserveCount - 1;
    }
}
