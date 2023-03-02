// SPDX-License-Identifier: MIT
// based on https://solidity-by-example.org/app/english-auction/ 

/*

English auction for NFT.

Auction
- Seller of NFT deploys this contract.
- Auction lasts for 7 days.
- Participants can bid by depositing ETH greater than the current highest bidder.
- All bidders can withdraw their bid if it is not the current highest bid.
After the auction
- Highest bidder becomes the new owner of NFT.

*/

pragma solidity ^0.8.13;

interface IERC721 {
    function transferFrom(
        address,
        address,
        uint
    ) external;
}

interface IERC20 {
    function transferFrom(
        address from,
        address to,
        uint amount
    ) external returns(bool);
}

contract EnglishAuction {
    event Start();
    event Bid(address indexed sender, uint amount);
    event Withdraw(address indexed bidder, uint amount);
    event End(address winner, uint amount);

    IERC721 public nft;
    IERC20 public token;
    uint public nftId;

    address payable public seller;
    uint public endAt;
    bool public started;
    bool public ended;

    address public highestBidder;
    uint public highestBid;
    mapping(address => uint) public bids;
    mapping(address => mapping(address => bool)) public operators;

    constructor(
        address _nft,
        address _erc20,
        uint _nftId,
        uint _startingBid
    ) {
        nft = IERC721(_nft);
        nftId = _nftId;

        token = IERC20(_erc20);

        seller = payable(msg.sender);
        highestBid = _startingBid;
    }

    function start() external {
        require(!started, "started");
        require(!ended, "started");
        require(msg.sender == seller, "not seller");
        
        started = true;
        nft.transferFrom(msg.sender, address(this), nftId);
        endAt = block.timestamp + 7 days;

        emit Start();
    }

    function setOperator(address operator, bool trusted) external {
        operators[msg.sender][operator] = trusted;
    }

    function bidFor(address bidder, uint amount) external {
        _bid(bidder, msg.sender, amount);
    }

    function bid(uint amount) external {
        _bid(msg.sender, msg.sender, amount);
    }

    function _bid(address bidder, address payer, uint amount) internal {
        require(started, "not started");
        require(block.timestamp < endAt, "ended");
        uint previousBid = highestBid;
        
        // Should revert on lack of funds or approval
        require(token.transferFrom(payer, address(this), amount), "token transfer failed");

        // Crit bug - The credit calculation is wrong. Overcredits when caller is richer than the bidder, crediting the bidder.
        bids[bidder] = bids[msg.sender] + amount;
        highestBidder = bidder;
        highestBid = bids[highestBidder];

        require(bids[highestBidder] > previousBid, "new high value < highest");
        emit Bid(bidder, amount);
    }

    function _withdraw(address bidder, address recipient, uint256 amount) internal {
        require(bidder != highestBidder, "bidder cannot withdraw");
        bids[bidder] -= amount;

        // Real 
        require(token.transferFrom(address(this), recipient, amount), "token transfer failed");

        emit Withdraw(bidder, amount);
    }
    
    // A basic default withdraw function.
    function withdraw() external {
        _withdraw(msg.sender, msg.sender, bids[msg.sender]);
    }

    // A more controlled withdraw function with more features
    function withdrawAmount(address recipient, uint amount) external {
        _withdraw(msg.sender, recipient, amount);
    }

    // WithdrawFor() can be called by a trusted operator. Funds are transfered back to the operator.
    function withdrawFor(address operated, uint amount) external {
        require(operators[operated][msg.sender] || msg.sender == operated, "that operator was not allowed");
        _withdraw(operated, msg.sender, amount);
    }

    // The end() functions marks the end of the auction. It would transfer the nft to the winning bidder, and the highest bid to the seller.
    function end() external {
        require(started, "not started");
        require(block.timestamp >= endAt, "not ended");
        require(!ended, "ended");
        bool _success;

        ended = true;
        if (highestBidder != address(0)) {
            nft.transferFrom(address(this), highestBidder, nftId);
            _success = token.transferFrom(address(this), seller, bids[highestBidder]);
            require(_success, "token transfer failed");
        } else {
            nft.transferFrom(address(this), seller, nftId);
        }

        emit End(highestBidder, highestBid);
    }

}
