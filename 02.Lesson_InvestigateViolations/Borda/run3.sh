solc-select use 0.7.6
certoraRun BordaBug3.sol:Borda --verify Borda:Borda.spec \
--solc solc \
--send_only \
--msg "$1"
