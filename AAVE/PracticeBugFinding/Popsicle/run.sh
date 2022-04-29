certoraRun Popsicle.sol Receiver.sol \
	--verify Popsicle:Popsicle.spec \
	--solc solc8.4 \
	--optimistic_loop \
	--cloud \
	--msg "Popsicle bug" 


