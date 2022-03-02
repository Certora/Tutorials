# Properties

## Before

* cant bid on an auction that doesn't exist/was ended
* auction can only be started if it doesn't exist/was ended
* no one should have more than the total supply of tokens
* sum of all users' tokens should be less than total supply
* can only close an auction that exists
* auction end time can not be changed
* auction prize can not be changed
* auction owner can not be changed

## After

* no one should have more than the total supply of tokens
* sum of all users' tokens should be less than total supply
* can only close an auction that exists
* auction end time can not be changed after auction has started
* auction prize can not be changed after auction has started
* auction owner can never be changed (current implementation)
* cant decrease others' tokens
* totalSupply should never overflow
* bid expiry can not be decreased except with close() (becomes 0)
* winners balance only goes up with close() being called while they are the winner
