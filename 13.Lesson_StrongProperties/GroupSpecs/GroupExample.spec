
using DummyERC721 as NFT

methods {
    // getters 
    seller() returns (address)  envfree;
    endAt() returns (uint256)   envfree;
    started() returns (bool)    envfree;
    ended() returns (bool)     envfree;
    highestBidder() returns (address)  envfree;
    highestBid() returns (uint256) envfree;
    bids(address) returns (uint256) envfree;

    // state modifying 
    start(); 
    bid();
    withdraw();
    end();

    // DummyERC721 
    NFT.balanceOf(address) returns (uint256) envfree

    //eth balance
    ethBalanceOf(address) returns (uint256) envfree
}



rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false; 
}

