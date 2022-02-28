solc-select use 0.8.7
certoraRun MeetingSchedulerBug4.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--solc solc \
--send_only \
--msg "$1"