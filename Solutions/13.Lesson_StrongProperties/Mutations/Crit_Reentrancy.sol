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
    function safeTransferFrom(
        address from,
        address to,
        uint tokenId
    ) external;

    function transferFrom(
        address,
        address,
        uint
    ) external;
}

contract EnglishAuction {
    event Start();
    event Bid(address indexed sender, uint amount);
    event Withdraw(address indexed bidder, uint amount);
    event End(address winner, uint amount);

    IERC721 public nft;
    uint public nftId;

    address payable public seller;
    uint public endAt;
    bool public started;
    bool public ended;

    address public highestBidder;
    uint public highestBid;
    mapping(address => uint) public bids;

    constructor(
        address _nft,
        uint _nftId,
        uint _startingBid
    ) {
        nft = IERC721(_nft);
        nftId = _nftId;

        seller = payable(msg.sender);
        highestBid = _startingBid;
    }

    function start() external {
        require(!started, "started");
        require(msg.sender == seller, "not seller");

        nft.transferFrom(msg.sender, address(this), nftId);
        started = true;
        endAt = block.timestamp + 7 days;

        emit Start();
    }

    function bid() external payable {
        require(started, "not started");
        require(block.timestamp < endAt, "ended");
        uint previousBid = highestBid;

        bids[msg.sender] += msg.value;
        highestBidder = msg.sender;
        highestBid = bids[highestBidder];

        require(bids[highestBidder] > previousBid, "new high value < highest");
        emit Bid(msg.sender, msg.value);
    }

    function withdraw() external {
        require(msg.sender != highestBidder, "bidder cannot withdraw");
        // Crit bug - Reentrancy possible here
        uint bal = bids[msg.sender];
        payable(msg.sender).transfer(bal);
        bids[msg.sender] -= bal;

        emit Withdraw(msg.sender, bal);
    }

    function end() external {
        require(started, "not started");
        require(block.timestamp >= endAt, "not ended");
        require(!ended, "ended");

        ended = true;
        if (highestBidder != address(0)) {
            nft.safeTransferFrom(address(this), highestBidder, nftId);
            seller.transfer(bids[highestBidder]);
        } else {
            nft.safeTransferFrom(address(this), seller, nftId);
        }

        emit End(highestBidder, highestBid);
    }


    // just a getter for ethBalane
    function ethBalanceOf(address a) public view returns (uint256) {
        return a.balance; 
    }
}
