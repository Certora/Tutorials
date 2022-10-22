#!/bin/bash

# Has to be "GroupA", for example. Same as the file names suggest, case sensitive
GROUP_NAME = $1

# Happy flow should pass (unless bug?)
certoraRun GroupMutations/Mutation_GroupExample.sol DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Example" 

# Group A mutation
certoraRun GroupMutations/Mutation_GroupA.sol DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Mutation A" 


# Group B mutation
certoraRun GroupMutations/Mutation_GroupB.sol DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Mutation B" 

# Group C mutaiton
certoraRun GroupMutations/Mutation_GroupC.sol DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Mutation C" 

# Group D mutation
certoraRun GroupMutations/Mutation_GroupD.sol DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Mutation D"

# Group E mutation
certoraRun GroupMutations/Mutation_GroupE.sol DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec \
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Mutation E"



