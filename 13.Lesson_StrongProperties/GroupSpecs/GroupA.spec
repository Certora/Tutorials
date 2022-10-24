
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



rule sanity(method f) {
    env e;
    calldataarg args;
    f(e,args);
    assert false; 
}

rule whoChangedBalanceOf(env eB, env eF, method f) {
    address u;
    address a;
    calldataarg args;
    uint256 before = ethBalanceOf(a);
    f(eF, args);
    assert ethBalanceOf(a) == before, "balanceOf changed";
}

rule balancesCheck(env e, method f) {
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

rule highestBidderIntegrity(method f)
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
