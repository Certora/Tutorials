
using DummyERC721 as NFT

methods {
    // getters 
    seller() returns (address)  envfree;
    endAt() returns (uint256)   envfree;
    started() returns (bool)    envfree;
    ended() returns (bool)     envfree;
    highestBidder() returns (address)  envfree;
    highestBid() returns (uint256) envfree;
    startingBid() returns (uint256) envfree;
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

    onERC721Received(address, address, uint256, bytes) returns (bytes4) => NONDET
}
// rule sanity(method f) {
//     env e;
//     calldataarg args;
//     f(e,args);
//     assert false; 
// }

// invariant bidIncreasesFromStart()
//     highestBid() >= startingBid()

invariant highestBidMatchesBidder(address account)
    ( bids(account) <= highestBid() && (bids(account) == highestBid() => account == highestBidder()) )
        || highestBid() == startingBid() && highestBidder() == 0x0
{ preserved {
    // require bids(highestBidder()) == highestBid();
    require bids(account) < highestBid();
}}

rule monoticityOfBid(method f) {
    env e; calldataarg args;
    uint256 hBidPre = highestBid();

    f(e, args);

    uint256 hBidPost = highestBid();

    assert hBidPre != hBidPost => hBidPost > hBidPre, "bid did not increase";
}

// sellers balance must increase by highestBid and they must not receive the nft
// buyers balance must decrease by highestBid and they must receive the nft

// rule safeTransfers(method f, method g) {

//     require started();

//     // init values
//     address buyer; address seller;
//     require seller == seller();
//     uint256 buyer_balance_pre = ethBalanceOf(buyer);
//     uint256 seller_balance_pre = ethBalanceOf(seller);
//     uint256 nft_buyer_pre = NFT.balanceOf(buyer);
//     uint256 nft_seller_pre = NFT.balanceOf(seller);
//     uint256 nft_cc_pre = NFT.balanceOf(currentContract);


//     env e; calldataarg args1;
//     f(e, args1);

//     env eEnd;
//     end(e);

//     // calldataarg args2;
//     // g(e, args2);

//     // end values
//     uint256 buyer_balance_post = ethBalanceOf(buyer);
//     uint256 seller_balance_post = ethBalanceOf(seller);
//     uint256 nft_buyer_post = NFT.balanceOf(buyer);
//     uint256 nft_seller_post = NFT.balanceOf(seller);
//     uint256 nft_cc_post = NFT.balanceOf(currentContract);

//     // properties 
//     assert buyer == seller => buyer_balance_post == buyer_balance_pre && nft_seller_post == nft_seller_pre + 1, "pumped";
    
//     // needs fixes to account for already bidded
//     assert buyer != seller && buyer == highestBidder() => (nft_buyer_post == nft_buyer_pre + 1) && (buyer_balance_post <= buyer_balance_pre), "buyer lost funds and gained nft";

//     assert buyer != seller => nft_seller_pre == nft_seller_post && seller_balance_post == seller_balance_pre + highestBid(), "seller gained funds and lost nft";

//     assert nft_buyer_post == nft_buyer_pre - 1, "contract gave up nft";
// }

// accounts other than the highest bid must be able to withdraw funds, only up to what they initially deposited

// if your eth balance changes and your nft balance changes, then your balance changes exactly by highest bid and nft balance changes by 1

// calling end twice must revert

// rule doubleEndReverts() {
//     env e;
//     end(e);
//     assert ended(), "end sets ended";
//     end@withrevert(e);
//     assert lastReverted, "called end twice";
// }