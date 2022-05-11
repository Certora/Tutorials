pragma solidity ^0.8.7;

/** Meeting Scheduler Overview
 * @dev This contract simulates a meeting scheduler for various uses.
 * 
 * The scheduler follows a clear path through the different states of a meeting's life.
 * The system allows one to create a schedule, defining the start and end times of the meeting.
 * The scheduler also tracks the number of participants attending the meeting.
 *
 * The meetings in the system are going through the following states: 
 * - Before creation, they are classified as UNINITIALIZED.
 *
 * - At creation, the meeting's state changes to PENDING, the start and end times are set according to the 
 * organizer's order, and the number of participants is nullified.
 *
 * - Anybody can start a PENDING meeting if the start time has arrived (the meeting's status 
 * changes to STARTED).
 * -A meeting's owner be cancel it (changes to CANCELLED) by its owner. A meeting that has already
 * occurred can not be labeled CANCELLED.
 *
 * - When the end time arrives, a STARTED meeting becomes ENDED.
 */

interface IMeetingScheduler {
    
    enum MeetingStatus {
        UNINITIALIZED,
        PENDING,
        STARTED,
        ENDED,
        CANCELLED
    }

    struct ScheduledMeeting {
        uint256 startTime;
        uint256 endTime;
        uint256 numOfParticipents;
        address organizer;
        MeetingStatus status;
    }

    // Gets the status of a specified meetingId
    function getStateById(uint256 meetingId)
        external
        view
        returns (MeetingStatus);

    // Gets the start time of a specified meetingId
    function getStartTimeById(uint256 meetingId)
        external
        view
        returns (uint256);

    // Gets the end time of a specified meetingId
    function getEndTimeById(uint256 meetingId) external view returns (uint256);

    // Gets the number of participants of a specified meetingId
    function getNumOfParticipents(uint256 meetingId)
        external
        view
        returns (uint256);

    // Gets the organizer of a specified meetingId
    function getOrganizer(uint256 meetingId)
        external
        view
        returns (address);

    // Creates a registry of meetingId in the map and updates its details.
    function scheduleMeeting(
        uint256 meetingId,
        uint256 startTime,
        uint256 endTime
    ) external;

    // Changes the status of a meeting to STARTED
    function startMeeting(uint256 meetingId) external;

    // Changes the status of a meeting to CANCELLED if it hasn't started yet
    function cancelMeeting(uint256 meetingId) external;

    // Changes the status of a meeting to ENDED only if it occured and its end time has arrived
    function endMeeting(uint256 meetingId) external;

    // Increases a meeting's participants' count
    function joinMeeting(uint256 meetingId) external;
}
