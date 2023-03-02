/*
   This is a specification file for EnglishAuction's formal verification
   using the Certora prover.
 */
 
 
 import "erc20.spec"

// Reference from the spec to additional contracts used in the verification 
using DummyERC721A as NFT
using DummyERC20A as Token


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


    // erc721
    safeTransferFrom(address, address, uint256)                             => DISPATCHER(true)
    NFT.balanceOf(address) returns (uint256)                                envfree
    NFT.ownerOf(uint256) returns (address)                                  envfree
    /* NONDET implies that the function is treated as a non state changing 
       function that returns arbitrary value */ 
    onERC721Received( address,address,uint256,bytes) returns (address)      => NONDET

    //erc20
    Token.balanceOf(address)                                                envfree
}




/*-----------------------------------------------
|              Ghosts and hooks                 |
-----------------------------------------------*/

/* This ghost is like an additional variable that tracks changes to the bids mapping */
ghost mathint sumBids {
    init_state axiom sumBids == 0 ;
}
    
/* whenever bids[user] is updated to newValue where previously it held oldValue
   update sumBind */
hook Sstore bids[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumBids = sumBids + newValue - oldValue;
}



/*-----------------------------------------------
|                  Functions                    |
-----------------------------------------------*/


function withdrawHelper(env e, method f, address user) returns bool {
    bool isReverted;

    if (f.selector == withdraw().selector){
        require e.msg.sender == user;
        withdraw@withrevert(e);
        isReverted = lastReverted;
        return isReverted;

    } else if (f.selector == withdrawAmount(address, uint).selector) {
        address recipient; uint amount;
        require e.msg.sender == user;
        withdrawAmount@withrevert(e, recipient, amount);
        isReverted = lastReverted;
        return isReverted;

    } else {
        address operated; uint amount;
        require operated == user;
        withdrawFor@withrevert(e, operated, amount);
        isReverted = lastReverted;
        return isReverted;
    }
}


function bidHelper(env e, method f) {
    uint256 amount;

    if (f.selector == bid(uint).selector){
        require e.msg.sender != currentContract;
        bid(e, amount);
        
    } else if (f.selector == bidFor(address, uint).selector) {
        address bidder;
        require bidder != currentContract;
        bidFor(e, bidder, amount);

    } else {
        calldataarg args;
        f(e, args);
    }
}


function callBidFunction(method f, env e, uint amount, address bidder) returns bool {
    if (f.selector == bid(uint).selector ) {
        bid@withrevert(e, amount);
        return !lastReverted; 
    }
    else {
        bidFor@withrevert(e, bidder, amount);
        return !lastReverted;
    }
}


function callFunctionHelper(env e, method f, address operator, address bidder) {
    uint256 amount;

    if (f.selector == withdrawAmount(address, uint).selector) {
        require e.msg.sender == operator;
        withdrawAmount(e, bidder, amount);
    } else if  (f.selector == withdrawFor(address, uint).selector ){
        require e.msg.sender == operator;
        withdrawFor(e, bidder, amount);
    }    
    else if (f.selector == bidFor(address, uint).selector) {
        require e.msg.sender == operator;
        bidFor(e, bidder, amount);
    } 
    else if (f.selector == end().selector) {
        require bidder != highestBidder() && bidder != seller() 
                    && operator != highestBidder() && operator != seller();
        end(e);
    }
    else {
        calldataarg args;
        f(e, args);
    }
}



/*-----------------------------------------------
|                  Properties                   |
-----------------------------------------------*/


/*****************/
/*** Unit Test ***/
/*****************/

/* Property: Integrity of end() time
   
   Description: Impossible to end earlier (version 1 - end() could be successfully executed only if assert is true)

   This is an example of a simple unit test: for all states, for all block.timestamp 
   if end() succeeded then block.timestamp must be at least endAt()
   Note that as default only non reverting paths are reasoned 

*/
rule integrityOfEndTime(env e) {
    end(e);

    assert e.block.timestamp >= endAt(), "ended before endAt"; 
}

/* Property: Integrity of end() time
   
   Description: Impossible to end earlier (version 2 - end() should revert under required condition)

   Same property as above but implemented with taking into account reverting path and reasoning about the case of lastReverted

*/
// Impossible to end earlier (
rule impossibleToEndEarlier(env e, method f) {
    require e.block.timestamp < endAt();

    end@withrevert(e);

    assert lastReverted, "ended before endAt";
}

// Impossible to restart (fails reachability check for start() in f() because it cannot be performed under invariant conditions)
rule noDoubleStart(method f) {
    env e1; env e2; env eF;

    start(e1);                  // start the auction

    calldataarg args;
    f(eF,args);                 // calling all functions to see if it's possible to allow start() to be called successfully again

    start@withrevert(e2);       // trying to start again

    assert lastReverted;
}


// Impossible to end twice - the same logic as in `noDoubleStart` - (fails reachability check for end() and start() because it cannot be performed under invariant conditions)
rule noDoubleEnd(method f) {
    env e1; env e2; env eF;

    end(e1);
    
    calldataarg args;
    f(eF,args);

    end@withrevert(e2);

    assert lastReverted;
}


// Auction flag `ended` cannot be set to false if it's not time for it (fails reachability check for end() because it cannot be performed under invariant conditions)
rule noTimeToEnd(env e, method f) {
    require e.block.timestamp < endAt() <=> !ended();

    calldataarg args;
    f(e,args);

    assert e.block.timestamp < endAt() <=> !ended();
}


// check correctness of bid functions:
// 1 - if bid succeeded, the bidder should become the highestBidder and their balance should beupdated respectively
// 2 - if the sum of bidder's previous bids and current bid is less than current highestBid, then bid should revert
rule integrityOfBid(env e, method f) 
    filtered { f -> 
                f.selector == bidFor(address, uint).selector 
                || f.selector == bid(uint).selector 
    } 
{
    uint amount;
    address bidder;
    uint currentHighestBid = highestBid();
    uint bidBefore = bids(bidder);

    if (f.selector == bid(uint).selector ) {
        require bidder == e.msg.sender; 
    }
    
    bool success = callBidFunction(f, e, amount, bidder); 
 
    assert success => (bids(bidder) == bidBefore + amount && bidder == highestBidder());
    assert bidBefore + amount < currentHighestBid => !success;
}


// check correctness of withdraw():
// 1 - check that current highestBidder cannot withdraw
// 2 - if withdraw succeeded, then user's bids should be 0 and token balance should increase respectively
rule integrityOfWithdraw(env e, method f) 
{
    address bidder;
    address currentHighestBidder = highestBidder();
    uint bidBefore = bids(e.msg.sender);
    uint balanceBefore = Token.balanceOf(e.msg.sender);

    require (e.msg.sender != currentContract); // nice to show first the counter example

    withdraw@withrevert(e);

    assert e.msg.sender == currentHighestBidder => lastReverted;
    assert !lastReverted => bids(e.msg.sender) == 0 
                    && Token.balanceOf(e.msg.sender) == balanceBefore + bidBefore;
}


// If user's bids were decreased, they can't be the highestBidder
rule integrityOfAllWithdraws(env e, method f) 
{
    address bidder;
    address currentHighestBidder = highestBidder();
    uint bidBefore = bids(bidder);

    calldataarg args;
    f(e, args);

    assert bids(bidder) < bidBefore => bidder != currentHighestBidder;
}


// highestBidder cannot withdraw
rule highestBidderFundsLocked(env e, method f) 
    filtered { f -> 
        f.selector == withdraw().selector 
        || f.selector == withdrawAmount(address, uint).selector 
        || f.selector == withdrawAmount(address, uint).selector 
    } 
{
    address user;

    bool isReverted = withdrawHelper(e, f, user);

    assert user == highestBidder() => isReverted, "Remember, with great power comes great responsibility.";
}



/***********************/
/***** Valid State *****/
/***********************/


// If nobody made a bid, then all bids should be 0
invariant zeroHighestBid(address other)
    (highestBid() == 0 || highestBidder() == 0) => bids(other) == 0 
    {
        preserved bidFor(address bidder, uint amount) with (env e) {
            require bidder != 0; // we can prove this
        }
    }


// check highestBidder correlation with highestBid from bids mapping
invariant highestBidVSBids(address a) 
    (highestBidder() == a  => bids(a) == highestBid()) ||
    (highestBidder() == 0) 


// If a user isn't the highestBidder, they should have less bids than highestBid
invariant integrityOfHighestBidStep3(address other) 
    (highestBid() > 0 && other != highestBidder()) => 
                bids(other) < highestBid() 
    {
        preserved {
            requireInvariant highestBidVSBids(other);
            requireInvariant zeroHighestBid(other);
        }
    }


// Nobody can have more bids than highestBid
invariant integrityOfHighestBidWeaker(address any) 
    bids(any) <= highestBid() 


/****************************/
/***** State Transition *****/
/****************************/


// once auction was ended it always remains ended
rule onceEndedAlwaysEnded(method f) {
    env e;
    calldataarg args; 

    bool before = ended();
    f(e, args);
    assert before => ended();
}


// started iff contract holds nft:
// 1 - if start() succeeded, auction contract must hold NFT 
// 2 - if the auction was started, start() was called
rule onStarted(method f) {
    env e;
    calldataarg args; 

    bool startedBefore = started();
    f(e, args);

    assert !startedBefore && started() => NFT.balanceOf(currentContract) >= 1 
                                            && NFT.ownerOf(nftId()) == currentContract;
    assert !startedBefore && started() => f.selector == start().selector;
}


// after start(), `start` is true and `end` is false
rule flagsAfterStart(env e, method f) {

    bool isStar = started();
    bool isEnd = ended();

    start(e);

    bool isStarted = started();
    bool isEnded = ended();

    assert isStarted && !isEnded, "Remember, with great power comes great responsibility.";
}


// after end(), both state flags are true 
rule flagsAfterEnd(env e, method f) {

    bool isStar = started();
    bool isEnd = ended();

    end(e);

    bool isStarted = started();
    bool isEnded = ended();

    assert isStarted && isEnded, "Remember, with great power comes great responsibility.";
}



/*****************************/
/***  Variable Transition ****/
/*****************************/

/* 
   Property: Monotonicity of highest bid 
   Description: highestBid can't decrease (if we consider only bid functions, can use >)

   Implemented as a parametric rule, a rule that is verified on all external\public functions of the contract
*/

rule monotonicityOfHighestBid(method f) {
    uint before = highestBid();
    
    env e;
    calldataarg args; 
    f(e, args);

    assert highestBid() >= before;
}



/*******************/
/*** High Level ****/
/*******************/


// only balance of a specific user can change after a function call
rule noChangeToOther(method f, address bidder) {
    env e;
    calldataarg args; 
    uint256 amount; address bidderFor;

    uint beforeBid = bids(bidder);

    if (f.selector == bidFor(address, uint).selector) {
        bidFor(e, bidderFor, amount);
    } 
    else {
        f(e, args);
    }

    uint afterBid = bids(bidder);

    assert afterBid != beforeBid => (bidder == e.msg.sender 
                                        || operators(bidder, e.msg.sender) == true 
                                        || bidderFor == bidder);
} 


// system should have at least the sum of all bids to be able to payback everybody
invariant solvency() 
    sumBids <= Token.balanceOf(currentContract) 
    filtered { f -> f.selector != end().selector } 
    {
        preserved with (env e) {
            require e.msg.sender != currentContract;
        }
    }


// user solvency  - the total assets of a user is maintained beside the seller and the highestBidder 
rule totalAssetsOfUser(method f) {
    env e;
    uint amount;  
    address operator;
    address bidder;

    require bidder != operator;
    require bidder != currentContract;
    require operator != currentContract;

    mathint totalAssertBefore = bids(bidder) + Token.balanceOf(bidder) 
                                    + bids(operator) + Token.balanceOf(operator); 

    callFunctionHelper(e, f, operator, bidder);

    mathint totalAssertAfter = bids(bidder) + Token.balanceOf(bidder) 
                                + bids(operator) + Token.balanceOf(operator);

    assert totalAssertAfter == totalAssertBefore ;
}



/**********************/
/*** Risk Analysis ****/ 
/**********************/


// nft remains at the system until the end of auction
rule lifeOfNFT(env e, method f) {
    address nftOwnerBefore = NFT.ownerOf(nftId());

    require currentContract == nftOwnerBefore;
    require currentContract != highestBidder();

    bidHelper(e, f);

    address nftOwnerAfter = NFT.ownerOf(nftId());

    assert nftOwnerAfter == highestBidder() && currentContract != seller() => f.selector == end().selector, "Remember, with great power comes great responsibility.";
    assert nftOwnerBefore == nftOwnerAfter && currentContract != seller() => f.selector != end().selector;
}


// cannot withdraw more with withdrawAmount() than bids you have 
rule mortalWithdrawAmount(env e, method f) {
    address recipient; 
    uint256 amount;

    uint256 bidBefore = bids(e.msg.sender);

    withdrawAmount@withrevert(e, recipient, amount);

    assert bidBefore < amount => lastReverted, "Remember, with great power comes great responsibility.";
}


// At the end of auction a seller will get NFT back or get tokens
rule sellerGetsPayed(env e) {
    uint256 balanceBefore = Token.balanceOf(seller());
    uint nftBalanceBefore = NFT.balanceOf(seller());
    uint toSeller = highestBid();

    require seller() != currentContract;  
    requireInvariant highestBidVSBids(highestBidder());

    end(e);

    assert Token.balanceOf(seller()) == toSeller + balanceBefore 
                || NFT.balanceOf(seller()) == nftBalanceBefore + 1;
}

rule changeToNFTOwner(env e, method f) {
    address nftOwnerBefore = NFT.ownerOf(nftId()); /* reference to another contract */

    address operator; address bidder;

    callFunctionHelper(e, f, operator, bidder);    /* use of a CVL function just for fun */

    address nftOwnerAfter = NFT.ownerOf(nftId());

    assert nftOwnerAfter != nftOwnerBefore  => ( f.selector == end().selector || f.selector == start().selector );
}