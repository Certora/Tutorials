
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


rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false; 
}


rule startAllowedOnlyOnce(method f){
    env e; env e1;
    calldataarg args; calldataarg args1;
    start(e,args);
    start@withrevert(e1,args1);
    bool reverted = lastReverted;
    assert reverted;
 }


