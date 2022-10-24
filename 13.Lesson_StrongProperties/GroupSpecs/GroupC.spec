
using DummyERC721 as NFT

methods {
    // getters 
    seller() returns (address)  envfree;
    nftId()        returns (uint256) envfree;
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

    onERC721Received( address, address, uint256, bytes ) returns (bytes4) => DISPATCHER(true)
}


rule sanity_should_fail()
{
    env e;
    require e.msg.sender != 0x1ee7;
    end(e);
    assert false;
}


rule bidWithdraw() {
    env eA;
    address a;
    address b;
    address c;
    require c != currentContract;
    require a != currentContract;
    require b != currentContract;
    require c != a;
    require c != b;
    require a != b;

    uint256 BalanceAOld = ethBalanceOf(a);
    uint256 BalanceBOld = ethBalanceOf(b);
    require eA.msg.sender == a;
    uint256 bidAAddition = eA.msg.value;
    uint256 oldAbid = bids(a);
    bid(eA);
    require bids(b) < bids(a);
    assert ethBalanceOf(a) == BalanceAOld - bidAAddition;
    assert highestBidder() == a && highestBid() == oldAbid + bidAAddition && bids(a) == highestBid();
    assert BalanceBOld == ethBalanceOf(b);
    env eB;
    require eB.msg.sender == b;
    uint256 bidBAddition = eB.msg.value;
    uint256 newAbalance = ethBalanceOf(a);
    uint256 oldBbid = bids(b);
    bid(eB);
    assert ethBalanceOf(b) == BalanceBOld - bidBAddition;
    assert highestBidder() == b && highestBid() == oldBbid + bidBAddition && bids(b) == highestBid();
    assert newAbalance == ethBalanceOf(a);

    env eA2;
    require eA2.msg.sender == a;
    
    uint256 CBalnce = ethBalanceOf(c);
    uint256 bBalanceBeforeWithdraw = ethBalanceOf(b);
    withdraw(eA2);
    assert CBalnce == ethBalanceOf(c);
    assert BalanceAOld + oldAbid == ethBalanceOf(a);
    assert bBalanceBeforeWithdraw == ethBalanceOf(b);
    assert bids(a) == 0;
    
}

