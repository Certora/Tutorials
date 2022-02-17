pragma solidity ^0.8.7;

/** Meeting Scheduler Overview
 * @dev This contract simulates a meeting scheduler for various uses.
 * 
 * The scheduler follows a very clear path through different states of a meeting's life.
 * The system allows one to create a schedule, defining the start and end times of the meeting.
 * The scheduler also tracks the number of participants attending the meeting.
 *
 * - The meetings in the system are going through the following states - before creation, they are
 * classified as UNINITIALIZED.
 *
 * - At creation, the state changes to PENDING, the start and end times are set according to 
 * the organizer's order, and the number of participants is nullified.
 *
 * - Anybody can start (change it to STARTED) a PENDING meeting. The owner of A PENDING meeting 
 * can cancel it (change it to CANCELLED) by the owner. A meeting that has already occurred can 
 * not be labeled CANCELLED.	
 *
 * - If the meeting has already started and the end time has arrived, anybody can change its 
 * status to ENDED.
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

    // Creates a registry of meetingId in the map and updating its details.
    function scheduleMeeting(
        uint256 meetingId,
        uint256 startTime,
        uint256 endTime
    ) external;

    // Changes the status of a meeting to STARTED
    function startMeeting(uint256 meetingId) external;

    // Changes the status of a meeting to CANCELLED if it hasn't started yet
    function cancelMeeting(uint256 meetingId) external;

    // Changes the status of a meeting to ENDED only if it really occurred
    function endMeeting(uint256 meetingId) external;

    // Increases a meeting's participants' count by one
    function joinMeeting(uint256 meetingId) external;
}
