/*  Representing enums

    enums are supported by the Certora Verification Language (CVL), 
    according to thier low level representation - uint8.
    in our case:
        -UNINITIALIZED = 0
        -PENDING = 1
        -STARTED = 2
        -ENDED = 3
        -CANCELLED = 4
    So for exmple if we write 'state == 0' we mean 'state == UNINITIALIZED'
    or 'state % 2 == 1' we mean 'state == PENDING || state == ENDED'.

    We will learn more about supported data structures in future lessons.
    For now, follow the above explanation to pass this exercise.
 */


// Checks that when a meeting is created, the planned end time is greater than the start time
rule startBeforeEnd(method f, uint256 meetingId, uint256 startTime, uint256 endTime) {
	env e;
    scheduleMeeting(e, meetingId, startTime, endTime);
    uint256 scheduledStartTime = getStartTimeById(e, meetingId);
    uint256 scheduledEndTime = getEndTimeById(e, meetingId);

	assert scheduledStartTime < scheduledEndTime, "the created meeting's start time is not before its end time";
}


// Checks that a meeting can only be started within the defined range [startTime, endTime]
rule startOnTime(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(e, meetingId);
	f(e, args); // call only non reverting paths to any function on any arguments.
	uint8 stateAfter = getStateById(e, meetingId);
    uint256 startTimeAfter = getStartTimeById(e, meetingId);
    uint256 endTimeAfter = getEndTimeById(e, meetingId);
    
	assert (stateBefore == 1 && stateAfter == 2) => startTimeAfter <= e.block.timestamp, "started a meeting before the designated starting time.";
	assert (stateBefore == 1 && stateAfter == 2) => endTimeAfter > e.block.timestamp, "started a meeting after the designated end time.";
	
}


// Checks that state transition from STARTED to ENDED can only happen if endMeeting() was called
// @note read again the comment at the top regarding f.selector
rule checkStartedToStateTransition(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(e, meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(e, meetingId);
	
	assert (stateBefore == 2 => (stateAfter == 2 || stateAfter == 3)), "the status of the meeting changed from STARTED to an invalid state";
	assert ((stateBefore == 2 && stateAfter == 3) => f.selector == endMeeting(uint256).selector), "the status of the meeting changed from STARTED to ENDED through a function other then endMeeting()";
}


// Checks that state transition from PENDING to STARTED or CANCELLED can only happen if
// startMeeting() or cancelMeeting() were called, respectively
// @note read again the comment at the top regarding f.selector
rule checkPendingToCancelledOrStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(e, meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(e, meetingId);
	
	assert (stateBefore == 1 => (stateAfter == 1 || stateAfter == 2 || stateAfter == 4)), "invalidation of the state machine";
	assert ((stateBefore == 1 && stateAfter == 2) => f.selector == startMeeting(uint256).selector), "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting()";
	assert ((stateBefore == 1 && stateAfter == 4) => f.selector == cancelMeeting(uint256).selector), "the status of the meeting changed from PENDING to CANCELLED through a function other then cancelMeeting()";
}


// Checks that the number of participants in a meeting cannot be decreased
rule monotonousIncreasingNumOfParticipants(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require getStateById(e, meetingId) == 0 => getNumOfParticipents(e, meetingId) == 0;
	uint256 numOfParticipantsBefore = getNumOfParticipents(e, meetingId);
	f(e, args);
    uint256 numOfParticipantsAfter = getNumOfParticipents(e, meetingId);

	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
}
