# #!/bin/bash

# # Has to be "GroupA", for example. Same as the file names suggest, case sensitive
# GROUP_NAME = $1

# Happy flow should pass (unless bug?)
certoraRun GroupMutations/Mutation_GroupExample.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/GroupUnified.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - GroupUnified vs Example" --send_only

# Group A mutation
certoraRun GroupMutations/Mutation_GroupA.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/GroupUnified.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - GroupUnified vs Mutation A" --send_only


# Group B mutation
certoraRun GroupMutations/Mutation_GroupB.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/GroupUnified.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - GroupUnified vs Mutation B" --send_only

# Group C mutaiton
certoraRun GroupMutations/Mutation_GroupC.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/GroupUnified.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - GroupUnified vs Mutation C" --send_only

# Group D mutation
certoraRun GroupMutations/Mutation_GroupD.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/GroupUnified.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - GroupUnified vs Mutation D" --send_only

# Group E mutation
certoraRun GroupMutations/Mutation_GroupE.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/GroupUnified.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - GroupUnified vs Mutation E" --send_only


