rule numEventsIncrease(method f) {
    env e;
    calldataarg args;
    uint16 numEventsBefore = numEvents(e);
    f(e, args);
    uint16 numEventsAfter = numEvents(e);
    assert (numEventsAfter > numEventsBefore) => (numEventsBefore == numEventsAfter - 1 && f.selector == createEvent(uint64, uint16).selector);
}

rule ticketsRemainingDecrease(uint16 eventId, method f) {
    env e;
    calldataarg args;
    uint16 ticketsRemainingBefore = eventsMap(eventId).ticketsRemaining;
    f(e, args);
    uint16 ticketsRemainingAfter = eventsMap(eventId).ticketsRemaining;
    assert (ticketsRemainingAfter < ticketsRemainingBefore) => (ticketsRemainingAfter == ticketsRemainingBefore - 1 && f.selector == buyNewTicket(uint16, address).selector);
}

rule buyNewTicketDecrease(uint16 eventId) {
    env e;
    calldataarg args;
    uint16 ticketsRemainingBefore = eventsMap(eventId).ticketsRemaining;
    buyNewTicket(e, eventId, e.msg.sender);
    uint16 ticketsRemainingAfter = eventsMap(eventId).ticketsRemaining; 
    assert ticketsRemainingAfter == ticketsRemainingBefore - 1;
}

rule buyOfferedTicketDontDecrease(uint16 eventId, uint16 ticketId) {
    env e;
    calldataarg args;
    uint16 ticketsRemainingBefore = eventsMap(eventId).ticketsRemaining;
    buyOfferedTicket(e, eventId, ticketId, e.msg.sender);
    uint16 ticketsRemainingAfter = eventsMap(eventId).ticketsRemaining;
    assert ticketsRemainingAfter == ticketsRemainingBefore;
}

/* how to deal with mapping of struct that has mapping in it?
rule buyerGetsTicketNew(uint16 eventId, address attendee) {
    env e;
    calldataarg args;
    uint16 ticketId = eventsMap(eventId).ticketsRemaining;
    address ticketOwnerBefore = eventsMap(eventId).attendees(ticketId);
    require ticketOwnerBefore != attendee;
    buyNewTicket(e, eventId, attendee);
    uint16 ticketOwnerAfter = eventsMap(eventId).attendees(ticketID);
    require ticketOwnerAfter == attendee;
}

rule buyerGetsTicketOffer(uint16 eventId, address attendee) {
    env e;
    calldataarg args;
    uint16 ticketId = eventsMap(eventId).ticketsRemaining;
    uint16 ticketOwnerBefore = eventsMap(eventId).attendees(ticketID);
    require ticketOwnerBefore != attendee;
    buyOfferedTicket(e, uint16 eventId, uint16 ticketId, address attendee);
    uint16 ticketOwnerAfter = eventsMap(eventId).attendees(ticketID);
    require ticketOwnerAfter == attendee;
}
*/