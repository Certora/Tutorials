certoraRun ReserveList.sol:ReserveList --verify ReserveList:Reserve.spec \
--solc solc8.7 \
--optimistic_loop \
--loop_iter 3 \
--send_only \
--msg "ReserveList Buggy"

# --optimistic_loop and --loop_iter 3 are flags that handle loops.
# They are needed here, but don't mind them, you will learn about loop handling in a future lesson.