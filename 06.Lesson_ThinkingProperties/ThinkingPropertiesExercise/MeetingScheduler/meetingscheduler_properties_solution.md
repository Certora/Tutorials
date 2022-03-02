# Properties For MeetingScheduler

```ruby
- `UNINITIALIZED` - is defined as `meetings[meetingId].status == 0`.
- `PENDING` - is defined as `meetings[meetingId].status == 1`.
- `STARTED` - is defined as `meetings[meetingId].status == 2`.
- `ENDED` - is defined as `meetings[meetingId].status == 3`.
- `CANCELLED` - is defined as `meetings[meetingId].status == 4`.
```

1. ***State transition*** UNINITIALIZED => PENDING only, and only with correct startTime and endTime inputs. startTime should be greater than `block.timestamp` and endTime should be greater than startTime.
2. ***State transition*** PENDING => STARTED or PENDING => CANCELLED only. If PENDING => STARTED then startMeeting() was called while the `block.timestamp` was between startTime and endTime.
3. ***State transition*** STARTED => ENDED only
4. ***Variable transition*** numberOfParticiants should only increase for a meeting while it is in STARTED state
5. ***High-level*** the total of all meetings that are not UNINITIALIZED should equal the number of times that scheduleMeeting was called
6. ***Unit tests*** calling joinMeeting on a STARTED meeting should always increase the numberOfParticipants by 1
7. ***Valid state*** a meeting should only be in UNINITIALIZED state if scheduleMeeting hasn't been called with its meetingId

</br>

---

## Prioritizing

</br>

### High Priority

- No properties are high priority as there are no funds at risk

### Medium Priority

- property 1, 2 and 3 are medium priority because they are fundamental to the meetingScheduler working as intended. If there are other ways to start, end or cancel a meeting then they can be started and cancelled out of order which may mess up peoples calenders.
- property 4 and 6 are medium because if someone is able to increase the number of participants for non-started meetings incorrectly they can potentially boost this number which may make their meeting look more important.

### Low Priority

- property 5 and 7 are low priority. If they are broken the total number of meetings can be off which may look bad when looking at meeting statistics later.
