solc-select use 0.8.4
certoraRun SpartaProtocolPool.sol:SpartaProtocolPool --verify SpartaProtocolPool:Sparta.spec \
--solc solc \
--send_only \
--msg "sparta run"

# --optimistic_loop and --loop_iter 3 are flags that handle loops.
# They are needed here, but don't mind them, you will learn about loop handling in a future lesson.

