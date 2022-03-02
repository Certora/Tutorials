# Properties For MeetingScheduler

1. ***Variable transition*** numEvents increases by 1 when createEvent is called
2. ***Variable transition*** after createEvent is called, eventsMap[numEvents].ticketsRemaining should only decrease (in reality new events can be started at old eventIds)
3. ***Unit tests*** number of tickets should decrease by 1 when buyNewTicket is called
4. ***Unit tests*** number of tickets shouldn't change when buyOfferedTicket is called
5. ***High-level*** buyer's address should replace sellers in eventsMap[_eventID].attendees[_ticketID] after buyOfferedTicket.
6. ***High-level*** Offers can only be bought once.

</br>

---

## Prioritizing

</br>

### High Priority

- property 5 is high priority since not changing the address to the buyers address will result in the buyer paying for nothing
- property 6 is high priority since offers being bought multiple times will result in someone not getting the ticket

### Medium Priority

- property 2, 3 and 4 are medium priority since having the wrong number of tickets can lead to more tickets being sold than initially expected

### Low Priority

- property 1 is low priority since having the wrong number of events will lead to a statistical error
