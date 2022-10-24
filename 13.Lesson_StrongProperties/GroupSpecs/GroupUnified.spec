
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

    onERC721Received( address, address, uint256, bytes ) returns (bytes4) => DISPATCHER(true)
}



// rule sanity(method f) {
//     env e;
//     calldataarg args;
//     f(e,args);
//     assert false; 
// }


rule GroupA_balancesCheck(env e, method f) {
    address winner; address random;

    require winner != random; require currentContract != random; require winner != currentContract;
    require winner != seller(); require seller() != random; require seller() != currentContract;
    require winner == highestBidder();
    require highestBidder() != 0;

    uint256 contractBefore = ethBalanceOf(currentContract);
    uint256 winnerBefore = ethBalanceOf(winner);
    uint256 randomBefore = ethBalanceOf(random);
    uint256 sellerBefore = ethBalanceOf(seller());
    
    end(e);

    uint256 contractAfter = ethBalanceOf(currentContract);
    uint256 winnerAfter = ethBalanceOf(winner);
    uint256 randomAfter = ethBalanceOf(random);
    uint256 sellerAfter = ethBalanceOf(seller());

    assert randomBefore == randomAfter;
    assert contractBefore == to_uint256(contractAfter + bids(highestBidder()));
    assert winnerBefore == winnerAfter;
    assert sellerBefore == to_uint256(sellerAfter - bids(highestBidder()));
}

rule GroupA_highestBidderIntegrity(method f)
{ 
    env e;
    calldataarg args;
    address a;
    address b;
    address highBefore = highestBidder();
    
    require b != a;
    require highestBid() == bids(highBefore);
    require (a != highestBidder()) => bids(highestBidder()) >= bids(a);
    require (b != highestBidder()) => bids(highestBidder()) >= bids(b);
        
        f(e, args);

    // highest bidder didn't change
    if(highBefore == highestBidder()) {
        assert (a != highestBidder()) => bids(highestBidder()) >= bids(a);
        assert (b != highestBidder()) => bids(highestBidder()) >= bids(b);
    }
     // highest bidder changed to a.
    else if (a == highestBidder() && a != highBefore){
        assert bids(highestBidder()) > bids(highBefore);
        assert bids(highestBidder()) > bids(b);
    }
    assert highestBid() == bids(highestBidder()); 
}


rule GroupD_ownershipTransfer(method f){
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
            && (highestBidderAfter !=0 => highestBidderAfter == ownerAfter)
           //     (highestBidderAfter != 0 && highestBidder() == ownerAfter)  
          //      ||
          //      (highestBidder() == 0 && ownerAfter == seller())
           // )
        )
    )
    );
}

rule GroupD_startAllowedOnlyOnce(method f){
    env e; env e1;
    calldataarg args; calldataarg args1;
    start(e,args);
    start@withrevert(e1,args1);
    bool reverted = lastReverted;
    assert reverted;
 }


invariant GroupE_highestBidMatchesBidder(address account)
    ( bids(account) <= highestBid() && (bids(account) == highestBid() => account == highestBidder()) )
        || highestBid() == startingBid() && highestBidder() == 0x0
{ preserved {
    // require bids(highestBidder()) == highestBid();
    require bids(account) < highestBid();
}}

rule GroupE_monoticityOfBid(method f) {
    env e; calldataarg args;
    uint256 hBidPre = highestBid();

    f(e, args);

    uint256 hBidPost = highestBid();

    assert hBidPre != hBidPost => hBidPost > hBidPre, "bid did not increase";
}


rule GroupC_sanity_should_fail()
{
    env e;
    require e.msg.sender != 0x1ee7;
    end(e);
    assert false;
}


rule GroupC_bidWithdraw() {
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
