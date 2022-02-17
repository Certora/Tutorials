pragma solidity ^0.7.0;

/** Broda Election Overview
 * @dev This contract simulate a Borda election.
 * 
 *
 * The election system follows the following rules:
 *
 * - Every user with an Etheruem address can vote in the elections.
 * - A voter must register their address with some personal detail.
 * - Once a voter has registered, they can vote once to 3 distinct contenders as they wish.
 * - The voter's 1st choice gets 3 points, their 2nd choice gets 2 points, and their 3rd choice gets 1 point.
 * - The 3 contenders have to be registered as contenders.
 * - If a voter tries to vote a second time, they will be warned.
 * - If the voter reaches a 3rd attempt to vote, they will be blocked and punished.
 * - Contenders are allowed to vote as long as they follow all the rules specified above.
 *
 */

interface IBorda {

    struct Contenders {
        uint8 age;
        // true if the contender is registered
        bool registered;
        // points a candidate has recieved.
        uint256 points;
    }

    struct Voters {
        uint8 age;
        // true if the voter is registered
        bool registered;
        // stores if the voter has voted already
        bool voted;
        // count the number of times the voter has attempted to vote
        uint256 vote_attempts;
        // returns true if the voter is blocked
        bool black_listed;
    }

    // Gets the number of points a specified contender has
    function getPointsOfContender(address contender) external view returns(uint256);

    // Gets a boolean indication whether a voter has voted
    function hasVoted(address voter) external view returns(bool);

    // Gets the winner at this point of time, and the number of points they have
    function getWinner() external view returns(address, uint256);

    // Gets the full details of a specified voter
    function getFullVoterDetails(address voter) external view returns(uint8 age, bool registered, bool voted, uint256 vote_attempts, bool black_listed);
    
    // Gets the full details of a specified contender
    function getFullContenderDetails(address contender) external view returns(uint8 age, bool registered, uint256 points);

    // Registers a voter so they could cast a vote
    function registerVoter(uint8 age) external returns (bool);

    // Registers a contender so they could receive votes
    function registerContender(uint8 age) external returns (bool);

    /**
    * @dev sends the voting chocies of the sender and updates their contenders' points accordingly.
    */
    function vote(address first, address second, address third) external returns(bool);

}
