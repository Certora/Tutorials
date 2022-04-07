certoraRun ../04.Lesson_Declarations/MeetingScheduler/MeetingSchedulerFixed.sol:MeetingScheduler \
--verify MeetingScheduler:../04.Lesson_Declarations/MeetingScheduler/meetings.spec \
--solc solc8.7 \
--rule checkStartedToStateTransition \
--method "startMeeting(uint256)" \
--send_only \
--msg "$1"