/**
A general "Receiver" that can receive money, can be used as a harness for EOAs.
 */
contract Receiver {
    fallback() external payable { }

    function acceptEth() external payable returns (bool) { return true; }

    receive() external payable { }
}