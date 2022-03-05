solc-select use 0.8.4
certoraRun popsicle.sol:PopsicleFinance --verify PopsicleFinance:popsicle.spec \
--solc solc \
--optimistic_loop \
--send_only \
--msg "popsicle L08"

# --optimistic_loop and --loop_iter 3 are flags that handle loops.
# They are needed here, but don't mind them, you will learn about loop handling in a future lesson.

