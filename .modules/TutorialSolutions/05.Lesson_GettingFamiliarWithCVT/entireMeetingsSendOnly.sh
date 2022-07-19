certoraRun ../04.Lesson_Declarations/MeetingScheduler/MeetingSchedulerFixed.sol:MeetingScheduler \
--verify MeetingScheduler:../04.Lesson_Declarations/MeetingScheduler/meetings.spec \
--solc solc8.7 \
--send_only \
--msg "$1"