pragma solidity ^0.8.7;

interface IReserveList {
    
    /**
     * @dev Details on assets in reserve mapping
     * @param id - a unique id generated for the asset. IDs starts with one
     * @note that the given id to a reserve asset is its location (index) in the underlying map
     * @param token - the token address
     * @param fee - a constant fee associated with trading this asset
     */ 
    struct ReserveData {
        uint256 id;   
        address lpToken;
        address stableDebtToken;
        address varDebtToken;
        uint256 fee;
    }

    // Gets the token saved in underlyingList mapping according to input index
    function getTokenAtIndex(uint256 index) external view returns (address);

    // Gets the ID saved in reserved mapping according to input token id
    function getIdOfToken(address token) external view returns (uint256);

    // Gets the count of underlying assets in the list
    function getReserveCount() external view returns (uint256);

    // Adds a reserve to the list and updates its details
    function addReserve(address token, address stableToken, address varToken, uint256 fee) external;

    // Removes a specified reserve from the list.
    function removeReserve(address token) external;
}
