pragma solidity ^0.8.7;

import "./IMeetingScheduler.sol";

contract MeetingScheduler is IMeetingScheduler {

    mapping(uint256 => ScheduledMeeting) private meetings;

    function getStateById(uint256 meetingId)
        external
        view
        override
        returns (MeetingStatus)
    {
        return meetings[meetingId].status;
    }

    function getStartTimeById(uint256 meetingId)
        external
        view
        override
        returns (uint256 startTime)
    {
        return meetings[meetingId].startTime;
    }

    function getEndTimeById(uint256 meetingId)
        external
        view
        override
        returns (uint256 endTime)
    {
        return meetings[meetingId].endTime;
    }

    function getNumOfParticipents(uint256 meetingId)
        external
        view
        override
        returns (uint256 numOfParticipants)
    {
        return meetings[meetingId].numOfParticipants;
    }

    function getOrganizer(uint256 meetingId)
        external
        view
        override
        returns (address organizer)
    {
        return meetings[meetingId].organizer;
    }

    function scheduleMeeting(
        uint256 meetingId,
        uint256 startTime,
        uint256 endTime
    ) external override {
        require(
            meetings[meetingId].status == MeetingStatus.UNINITIALIZED,
            "meeting has already been scheduled"
        );
        require(
            startTime > block.timestamp,
            "invalid start time, meeting has to be scheduled in the future"
        );
        require(endTime > startTime, "meeting has to end after it starts");
        meetings[meetingId] = ScheduledMeeting({
            startTime: startTime,
            endTime: endTime,
            numOfParticipants: 0,
            organizer: msg.sender,
            status: MeetingStatus.PENDING
        });
    }

    function startMeeting(uint256 meetingId) external override {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(
            scheduledMeeting.status == MeetingStatus.PENDING,
            "can't start a meeting if it isn't pending"
        );
        require(
            block.timestamp < scheduledMeeting.endTime,
            "can't start a meeting after its end time"
        );
        meetings[meetingId].status = MeetingStatus.STARTED;
    }

    function cancelMeeting(uint256 meetingId) external override {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(msg.sender == scheduledMeeting.organizer,
                "only the organizer of a meeting can cancel it"
        );
        require(
            scheduledMeeting.status == MeetingStatus.PENDING,
            "meetings can be cancelled only if it's currently pending"
        );
        meetings[meetingId].status = MeetingStatus.CANCELLED;
    }

    function endMeeting(uint256 meetingId) external override {
        ScheduledMeeting memory scheduledMeeting = meetings[meetingId];
        require(
            scheduledMeeting.status == MeetingStatus.STARTED,
            "can't end a meeting if not started"
        );
        require(
            block.timestamp >= scheduledMeeting.endTime,
            "meeting cannot be ended unless its end time passed"
        );

        meetings[meetingId].status = MeetingStatus.ENDED;
    }

    function joinMeeting(uint256 meetingId) external override {
        ScheduledMeeting memory meeting = meetings[meetingId];
        require(
            meeting.status == MeetingStatus.STARTED,
            "can only join to a meeting that has started"
        );
        meetings[meetingId].numOfParticipants++;
    }
}
