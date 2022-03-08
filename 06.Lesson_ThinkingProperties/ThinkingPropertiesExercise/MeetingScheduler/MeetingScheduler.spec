rule reachPendingState(uint256 stateId, method f) {
    env e;
    calldataarg args;
    require getStateById(e, stateId) == 0;
    f(e, args);
    assert (getStateById(e, stateId) != 3 && getStateById(e, stateId) != 4, "reached unreachable state 3 or 4 from 0");
    assert (getStateById(e, stateId) == 1) => (f.selector == scheduleMeeting(uint256, uint256, uint256).selector);
    assert (getStartTimeById(e, stateId) < getEndTimeById(e, stateId)) && (getStartTimeById(e, stateId) > e.block.timestamp);
}

rule leavePendingState(uint256 stateId, method f) {
    env e;
    calldataarg args;
    require getStateById(e, stateId) == 1;
    f(e, args);
    assert (getStateById(e, stateId) != 0 && getStateById(e, stateId) != 3, "reached unreachable state 0 or 3 from 1");
    assert (getStateById(e, stateId) == 2) => (f.selector == startMeeting(uint256).selector && getStartTimeById(e, stateId) > e.block.timestamp && getEndTimeById(e, stateId) < e.block.timestamp);
    assert (getStateById(e, stateId) == 4) => (f.selector == cancelMeeting(uint256).selector);
}

rule reachEndedState(uint256 stateId, method f) {
    env e;
    calldataarg args;
    require getStateById(e, stateId) == 2;
    f(e, args);
    assert (getStateById(e, stateId) != 0 && getStateById(e, stateId) != 1 && getStateById(e, stateId) != 4, "reached unreachable state 0, 1, or 4 from 2");
    assert (getStateById(e, stateId) == 3) => (f.selector == scheduleMeeting(uint256, uint256, uint256).selector);
}

rule startedMeetingParticipantsOnlyIncrease(uint256 stateId, method f) {
    env e;
    calldataarg args;
    uint256 numOfParticipantsBefore = getNumOfParticipents(e, stateId);
    f(e, args);
    uint256 numOfParticipantsAfter = getNumOfParticipents(e, stateId);
    assert(numOfParticipantsAfter > numOfParticipantsBefore => (numOfParticipantsAfter == numOfParticipantsBefore + 1) && getStateById(e, stateId) == 2 && f.selector == joinMeeting(uint256).selector);
}

// this might be a invariant?
// 7. ***Valid state*** a meeting should only be in UNINITIALIZED state if scheduleMeeting hasn't been called with its meetingId