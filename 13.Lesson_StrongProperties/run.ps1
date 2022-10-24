#!/bin/bash

certoraRun.exe EnglishAuction.sol DummyERC721.sol --verify EnglishAuction:EnglishAuction.spec `
--solc solc8.13  --link EnglishAuction:nft=DummyERC721 --settings -optimisticFallback=true  `
--disableLocalTypeChecking `
--msg "EnglishAuction $1" 


# overcoming calls to EOAs that are not easily linked (essentialy a dispatcher logic for ETH-sending only calls).
# --settings -optimisticFallback=true  
# linking the nft to a apecific contract 
#--link EnglishAuction:nft=DummyERC721 