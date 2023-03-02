/*
   This is a specification file for EnglishAuction's formal verification
   using the Certora prover.
 */
 
 
 import "erc20.spec"

// Reference from the spec to additional contracts used in the verification. 
using DummyERC721A as NFT
using DummyERC20A as Token


/*
    Declaration of methods that are used in the rules. envfree indicate that
    the method is not dependent on the environment (msg.value, msg.sender, etc.).
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
|                  Properties                   |
-----------------------------------------------*/


/****************************** 
*           Unit Test         *
******************************/


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



/****************************** 
*       Variable Transition   *
******************************/

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


/****************************** 
*       State Transition      *
******************************/


/* Property: Once ended Always ended
   
   Description: If the auction is at ended state it stays ended after every possible transaction 

   Implemented with an implication which can be written as:

   if (before) {
      assert (ended());
   }
   else 
      assert (True);  <---- always hold 

*/
rule onceEndedAlwaysEnded(method f) {
    env e;
    calldataarg args; 

    bool before = ended();
    require (false);
    f(e, args);
    assert before => ended();
    
}

rule same(method f) {
     env e;
    calldataarg args; 

    require ended();
    f(e,args);
    assert ended(); 
}

/****************************** 
*        Valid State          *
******************************/

// If nobody made a bid, then all bids should be 0
invariant zeroHighestBid(address other)
    (highestBid() == 0 || highestBidder() == 0) => bids(other) == 0 
    {
        preserved bidFor(address bidder, uint amount) with (env e) {
            require bidder != 0; 
        }

        preserved bid(uint amount) with (env e) {
            require e.msg.sender != 0; 
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



/****************************** 
*       High Level            *
******************************/



/****************************** 
*       Risk Assessment       *
******************************/

/* Property: changeToNFTOwner
   
   Description: NFT Owner does not change except on end() and start()

   Here there is a call to the NFT contract. Also note the use of f.selector to reference a specific function

   This property can be strengthened 
*/
rule changeToNFTOwner(env e, method f) {
    address nftOwnerBefore = NFT.ownerOf(nftId()); /* reference to another contract */

    address operator; address bidder;

    callFunctionHelper(e, f, operator, bidder);    /* use of a CVL function just for fun */

    address nftOwnerAfter = NFT.ownerOf(nftId());

    assert nftOwnerAfter != nftOwnerBefore  => ( f.selector == end().selector || f.selector == start().selector );
}





/*-----------------------------------------------
|              Ghosts and hooks                 |
-----------------------------------------------*/

/* This ghost is like an additional variable that tracks changes to the bids mapping */
/* mathint are the whole range of integer values (unlimited) */
ghost mathint sumBids {
    init_state axiom sumBids == 0 ;
}
    
/* whenever bids[user] is updated to newValue where previously it held oldValue
   update sumBind */
hook Sstore bids[KEY address user] uint256 newValue (uint256 oldValue) STORAGE {
    sumBids = sumBids + newValue - oldValue;
}

// simple rule that uses the ghost and filters 

rule justUseGhost(method f) {
    mathint before = sumBids;
    env e;
    calldataarg args;
    f(e,args);
    assert sumBids != before => true;
}

/*-----------------------------------------------
|           Helper Functions                    |
-----------------------------------------------*/

/* These helper functions are example and can help in reasoning about the different cases */

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
    require e.msg.sender == operator;
    if (f.selector == withdrawAmount(address, uint).selector) {     
        withdrawAmount(e, bidder, amount);
    } else if  (f.selector == withdrawFor(address, uint).selector ){
        withdrawFor(e, bidder, amount);
    }    
    else if (f.selector == bidFor(address, uint).selector) {
        bidFor(e, bidder, amount);
    } 
    else if (f.selector == end().selector) {
        end(e);
    }
    else {
        calldataarg args;
        f(e, args);
    }
}
