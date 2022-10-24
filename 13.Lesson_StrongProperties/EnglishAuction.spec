
using DummyERC721 as NFT

methods {
    // getters 
    seller() returns (address)  envfree;
    nftId() returns (uint)  envfree;
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
    NFT.ownerOf(uint256) returns (address) envfree
    onERC721Received( address,address,uint256,bytes) returns (address) => NONDET
    //eth balance
    ethBalanceOf(address) returns (uint256) envfree
}



rule ownershipTransfer(method f){
    env e;
    calldataarg args;
    address ownerBefore;
    address ownerAfter;
    bool startedBefore;
    bool endedBefore;
    bool startedAfter;
    bool endedAfter;

    startedBefore = started();
    endedBefore = ended();
    ownerBefore = NFT.ownerOf(nftId());
    f(e,args);
    ownerAfter = NFT.ownerOf(nftId());
    startedAfter = started();
    endedAfter = ended();
    address highestBidderAfter;
    address sellerAfter;

    highestBidderAfter = highestBidder();
    sellerAfter = seller();

    assert(
    (ownerBefore != ownerAfter)
    =>
    ( // start and end conditions
        (f.selector == start().selector && ownerAfter == currentContract && ownerBefore == seller() ) ||
        (f.selector == end().selector && ownerBefore == currentContract )
    )
    &&
    ( f.selector == start().selector =>
        (
            !startedBefore && startedAfter 
            // && 
           // e.msg.sender == sellerAfter && 
           // highestBidderAfter == sellerAfter
        )
    )
    &&
    ( f.selector == end().selector => 
        (
            (startedBefore == startedAfter) && !endedBefore && endedAfter 
         //   && (
         //       (highestBidder() != 0 && highestBidder() == ownerAfter)  
          //      ||
          //      (highestBidder() == 0 && ownerAfter == seller())
           // )
        )
    )
    );
}

rule startAllowedOnlyOnce(method f){
    env e; env e1;
    calldataarg args; calldataarg args1;
    start(e,args);
    start@withrevert(e1,args1);
    bool reverted = lastReverted;
    assert reverted;
 }

