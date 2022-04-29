certoraRun PopsicleFixed.sol ../Receiver.sol  \
	--verify PopsicleFixed:PopsicleAnswer.spec \
	--solc solc8.4 \
	--optimistic_loop \
	--send_only \
	--cloud \
	--msg "PopsicleFixed : PopsilceAnswer.spec " 


certoraRun ../Popsicle.sol  ../Receiver.sol  \
	--verify Popsicle:PopsicleAnswer.spec \
	--solc solc8.4 \
	--optimistic_loop \
	--send_only \
	--cloud \
	--msg "Popsicle Buggy: PopsilceAnswer.spec " 


