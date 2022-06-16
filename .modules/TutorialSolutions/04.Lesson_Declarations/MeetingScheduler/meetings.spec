

methods{
    getStateById(uint256) returns (uint8) envfree
    getStartTimeById(uint256) returns (uint256) envfree
    getEndTimeById(uint256) returns (uint256) envfree
    getNumOfParticipents(uint256) returns (uint256) envfree
    getOrganizer(uint256) returns (address) envfree

    scheduleMeeting(uint256, uint256, uint256)
    startMeeting(uint256)
    cancelMeeting(uint256)
    endMeeting(uint256)
    joinMeeting(uint256) envfree
}

// A non existing meeting has default values for all its fields.
definition meetingUninitialized(uint256 meetingId) returns bool = 
        getStateById(meetingId) == 0 && getStartTimeById(meetingId) == 0 &&
        getEndTimeById(meetingId) == 0 && getNumOfParticipents(meetingId) == 0 &&
        getOrganizer(meetingId) == 0;

// A pending meeting - @note that a meeting can be pending long after the start & end time are passed.
// because of that reason we don't know much about the min/max values. We can, however, assume that they are non 0
// we will have to require this in the rules as a precondition.
definition meetingPending(uint256 meetingId) returns bool = 
        getStateById(meetingId) == 1 && getStartTimeById(meetingId) != 0 &&
        getEndTimeById(meetingId) > getStartTimeById(meetingId) && 
        getNumOfParticipents(meetingId) == 0 &&
        // @note that there is no requirment in the contract that enforce that, 
        // but we can require that in the spec as we know that address 0 cannot call functions.
        getOrganizer(meetingId) != 0;

// A started meeting - @note that a meeting can be in started state way after the end time is passed.
definition meetingStarted(env e, uint256 meetingId) returns bool = 
        getStateById(meetingId) == 2 && getStartTimeById(meetingId) <= e.block.timestamp &&
        getEndTimeById(meetingId) > getStartTimeById(meetingId) && 
        // Note that we don't know anything about the number of participants. 
        // We can write it explicitly as shown below or omit the line completly (should be more efficient).
        getNumOfParticipents(meetingId) >= 0 &&
        // @note that there is no requirment in the contract that enforce that, 
        // but we can require that in the spec as we know that address 0 cannot call functions.
        getOrganizer(meetingId) != 0;

// An ended meeting
definition meetingEnded(env e, uint256 meetingId) returns bool = 
        getStateById(meetingId) == 3 && getStartTimeById(meetingId) < e.block.timestamp &&
        (getEndTimeById(meetingId) > getStartTimeById(meetingId) && getEndTimeById(meetingId) <= e.block.timestamp) &&
        // Note that we don't know anything about the number of participants. 
        // We can write it explicitly as shown below or omit the line completly (should be more efficient).
        getNumOfParticipents(meetingId) >= 0 &&
        // @note that there is no requirment in the contract that enforce that, 
        // but we can require that in the spec as we know that address 0 cannot call functions.
        getOrganizer(meetingId) != 0;

// A cancelled meeting - @note that a meeting can be cancelled long after the start & end time are passed.
// For that reason we don't know much about the min/max values. We can, however, assume that they are non 0
// we will have to require this in the rules as a precondition.
definition meetingCancelled(uint256 meetingId) returns bool = 
        getStateById(meetingId) == 4 && getStartTimeById(meetingId) != 0 &&
        getEndTimeById(meetingId) > getStartTimeById(meetingId) && 
        // We can know for sure that no participants joined the meeting
        getNumOfParticipents(meetingId) == 0 &&
        // @note that there is no requirment in the contract that enforce that, 
        // but we can require that in the spec as we know that address 0 cannot call functions.
        getOrganizer(meetingId) != 0;


// Checks that when a meeting is created, the planned end time is greater than the start time
rule startBeforeEnd(method f, uint256 meetingId, uint256 startTime, uint256 endTime) {
	env e;
    scheduleMeeting(e, meetingId, startTime, endTime);
    uint256 scheduledStartTime = getStartTimeById(meetingId);
    uint256 scheduledEndTime = getEndTimeById(meetingId);

	assert scheduledStartTime < scheduledEndTime, "the created meeting's start time is not before its end time";
}


// Checks that a meeting can only be started within the the defined range [startTime, endTime]
rule startOnTime(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args); // call only non reverting paths to any function on any arguments.
	uint8 stateAfter = getStateById(meetingId);
    uint256 startTimeAfter = getStartTimeById(meetingId);
    uint256 endTimeAfter = getEndTimeById(meetingId);
    
	assert (stateBefore == 1 && stateAfter == 2) => startTimeAfter <= e.block.timestamp, "started a meeting before the designated starting time.";
	assert (stateBefore == 1 && stateAfter == 2) => endTimeAfter > e.block.timestamp, "started a meeting after the designated end time.";
	
}


// Checks that state transition from STARTED to ENDED can only happen if endMeeting() was called
// @note read again the comment in the top regarding f.selector
rule checkStartedToStateTransition(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
	
	assert (stateBefore == 2 => (stateAfter == 2 || stateAfter == 3)), "the status of the meeting changed from STARTED to an invalid state";
	assert ((stateBefore == 2 && stateAfter == 3) => f.selector == endMeeting(uint256).selector), "the status of the meeting changed from STARTED to ENDED through a function other then endMeeting()";
}


// Check that state transition from PENDING to STARTED or CANCELLED can only happen if
// startMeeting() or cancelMeeting() were called respectively
// @note read again the comment in the top regarding f.selector
rule checkPendingToCancelledOrStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);
	f(e, args);
    uint8 stateAfter = getStateById(meetingId);
	
	assert (stateBefore == 1 => (stateAfter == 1 || stateAfter == 2 || stateAfter == 4)), "invalidation of the state machine";
	assert ((stateBefore == 1 && stateAfter == 2) => f.selector == startMeeting(uint256).selector), "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting()";
	assert ((stateBefore == 1 && stateAfter == 4) => f.selector == cancelMeeting(uint256).selector), "the status of the meeting changed from PENDING to CANCELLED through a function other then cancelMeeting()";
}


// Checks that the number of participants in a meeting cannot be decreased
rule monotonousIncreasingNumOfParticipants(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
	uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);
	f(e, args);
    uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
}