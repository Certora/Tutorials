solc-select use 0.8.7
cd ../../04.Lesson_Declarations/Methods_Definitions_Functions/MeetingScheduler

certoraRun MeetingSchedulerFixed.sol:MeetingScheduler --verify MeetingScheduler:meetings.spec \
--rule startOnTime \
--method "getOrganizer(uint256)" \
--solc solc \
--send_only \
--msg "send_only, rule and method" 