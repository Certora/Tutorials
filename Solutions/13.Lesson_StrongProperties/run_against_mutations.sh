#!/bin/bash

# Has to be "GroupA", for example. Same as the file names suggest, case sensitive
GROUP_NAME=$1
SPEC_PATH=$2


# HappyFlow Sanity
certoraRun EnglishAuction.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs HappyFlow (should pass)" 

# Mutation Crit1
certoraRun Mutations/Crit_HigherBalanceFromBid.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 1_Crit_HigherBalanceFromBid" 

# Mutation Crit2
certoraRun Mutations/Crit_HighestCanWtihdraw.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 2_Crit_HighestCanWtihdraw" 

# Mutation Crit3
certoraRun Mutations/Crit_Reentrancy.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 3_Crit_Reentrancy" 

# Mutation Crit4
certoraRun Mutations/Crit_WithdrawAfterEnd.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 4_Crit_WithdrawAfterEnd" 

# Mutation High5
certoraRun Mutations/High_BidResetsBalance.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 5_High_BidResetsBalance" 

# Mutation High6
certoraRun Mutations/High_smallerBalanceFromBid.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 6_High_smallerBalanceFromBid" 

# Mutation Med7
certoraRun Mutations/Med_BidAfterEnd.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:$2 \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs 7_Med_BidAfterEnd" 


