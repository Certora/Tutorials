
pragma solidity ^0.6.0;

contract TicketDepot {  

	struct Event{  
		address owner;  
		uint64 ticketPrice;  
		uint16 ticketsRemaining;  
		mapping(uint16 => address) attendees;  
	} 

	struct Offering{  
		address buyer;
		uint64 price;
		uint256 deadline;
	} 

	uint16 numEvents;
	address public owner;  
	uint64 public transactionFee;  
	mapping(uint16 => Event) public eventsMap;
	mapping(bytes32 => Offering) offerings;

    // creates a "seller"
	function ticketDepot(uint64 _transactionFee) public {  
		transactionFee = _transactionFee;  
		owner = tx.origin;
        numEvents = 0;
	} 

    // creates an event with the specified number of tickets and price for sale
	function createEvent(uint64 _ticketPrice, uint16 _ticketsAvailable) public returns (uint16 eventID){         
		numEvents++;  
		eventsMap[numEvents].owner = tx.origin;  
		eventsMap[numEvents].ticketPrice = _ticketPrice;  
		eventsMap[numEvents].ticketsRemaining = _ticketsAvailable;
        eventID = numEvents;
	} 

    // reverts if the number of tickets available goes below 0
	modifier ticketsAvailable(uint16 _eventID){  
		_; 
		if (eventsMap[_eventID].ticketsRemaining == 65535) revert();  
	} 

    // buying a ticket as long as the buyer has enough money to pay for the ticket + fee
	function buyNewTicket(uint16 _eventID, address _attendee) ticketsAvailable(_eventID) public payable returns (uint16 ticketID){  
		if (msg.sender == eventsMap[_eventID].owner ||
            msg.value < eventsMap[_eventID].ticketPrice + transactionFee)
        {  
            revert();
		} 
        ticketID = eventsMap[_eventID].ticketsRemaining;
        eventsMap[_eventID].ticketsRemaining--;
		eventsMap[_eventID].attendees[ticketID] = _attendee;
        // paying the owner of the event the ticket price
		payable(eventsMap[_eventID].owner).transfer(eventsMap[_eventID].ticketPrice);
        // paying the owner of the depot the transaction fee
        payable(owner).transfer(transactionFee);
        
	} 

    // offer to resell your ticket
	function offerTicket(uint16 _eventID, uint16 _ticketID, uint64 _price, address _buyer, uint16 _offerWindow) public payable {  
		if (msg.sender != eventsMap[_eventID].attendees[_ticketID] ||
             msg.value < transactionFee) revert();  
        
		bytes32 offerID = keccak256(abi.encode(_eventID,_ticketID));  
		if (offerings[offerID].deadline != 0) revert();  
        // paying the depot the transaction fee - the seller pays the fee instead of the buyer
        payable(owner).transfer(transactionFee);
        offerings[offerID].buyer = _buyer;
		offerings[offerID].price = _price;
		offerings[offerID].deadline = block.number + uint256(_offerWindow);
	} 

    // buying a resale ticket
	function buyOfferedTicket(uint16 _eventID, uint16 _ticketID, address _newAttendee) public payable {  
		bytes32 offerID = keccak256(abi.encode(_eventID,_ticketID));  
		if (msg.value < offerings[offerID].price || 
                block.number >= offerings[offerID].deadline ||
                    (offerings[offerID].buyer != address(0) && offerings[offerID].buyer != msg.sender)) revert();

			// paying the current ticket holder (suggester)
            payable(eventsMap[_eventID].attendees[_ticketID]).transfer(offerings[offerID].price);
			eventsMap[_eventID].attendees[_ticketID] = _newAttendee;  
			delete offerings[offerID];  
	} 

} 
