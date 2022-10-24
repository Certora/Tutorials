# #!/bin/bash

# # Has to be "GroupA", for example. Same as the file names suggest, case sensitive
# GROUP_NAME = $1

# Happy flow should pass (unless bug?)
certoraRun GroupMutations/Mutation_GroupExample.sol:EnglishAuction DummyERC721.sol  \
--verify EnglishAuction:GroupSpecs/$1.spec --staging --solc solc8.13 \
--link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  \
--msg "Mutation Runs - $1 vs Example" --send_only

