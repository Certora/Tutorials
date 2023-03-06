
/*
   This is a specification file for EnglishAuction's formal verification
   using the Certora prover.
 */
 



/*
    Declaration of methods that are used in the rules. envfree indicate that
    the method is not dependent on the environment (msg.value, msg.sender).
    Methods that are not declared here are assumed to be dependent on env.
*/


methods {
    // auction getters 
    seller() returns (address)                                              envfree
    nftId() returns (uint)                                                  envfree
    nft() returns(address)                                                  envfree
    endAt() returns (uint256)                                               envfree
    started() returns (bool)                                                envfree
    ended() returns (bool)                                                  envfree
    highestBidder() returns (address)                                       envfree
    highestBid() returns (uint256)                                          envfree
    bids(address) returns (uint256)                                         envfree
    operators(address, address) returns (bool)                              envfree


}



// check highestBidder correlation with highestBid from bids mapping
invariant highestBidVSBids() 
    bids( highestBidder()) == highestBid()




// Nobody can have more bids than highestBid
invariant integrityOfHighestBid(address any) 
    bids(any) <= highestBid() 
