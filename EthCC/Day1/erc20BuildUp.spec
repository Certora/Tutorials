// Calling `transfer(recipient, amount)` results in `balanceOf(msg.sender)` 
// decreasing by `amount` and `balanceOf(recipient)` increasing by `amount`

// -- Step-1 -- //

// want to do this, what are these random variables?

rule transfer {
    transfer(recipient, amount);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-2 -- //

// defined the variables, but how do we know what the other variables are?

rule transfer {
    address myBalanceBefore = balanceOf(msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(recipient, amount);

    address myBalanceAfter = balanceOf(msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-3 -- //

// we defined the variables but can we actually do that?

rule transfer(address msg.sender, address recipient, uint256 amount) {
    address myBalanceBefore = balanceOf(msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(recipient, amount);

    address myBalanceAfter = balanceOf(msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-4 -- //

// we can also define them like this

rule transfer {
    address msg.sender; address recipient; uint256 amount;

    address myBalanceBefore = balanceOf(msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(recipient, amount);

    address myBalanceAfter = balanceOf(msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-5 -- //

// introduce environment variable

rule transfer(env e, address recipient, uint256 amount) {
    address myBalanceBefore = balanceOf(e.msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(e, recipient, amount);

    address myBalanceAfter = balanceOf(e.msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-6 -- //

// want a different environment variable in every rule

rule transfer(env e, env e1, env e2, env e3, env e4, address recipient, uint256 amount) {
    address myBalanceBefore = balanceOf(e1, e.msg.sender);
    address recipientBalanceBefore = balanceOf(e2, recipient);

    transfer(e, recipient, amount);

    address myBalanceAfter = balanceOf(e3, e.msg.sender);
    address recipientBalanceAfter = balanceOf(e4, recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-7 -- //

// want a different environment variable in every rule

methods {
    balanceOf(address) returns uint256 envfree
}

rule transfer(env e, address recipient, uint256 amount) {
    address myBalanceBefore = balanceOf(e.msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(e, recipient, amount);

    address myBalanceAfter = balanceOf(e.msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-8 -- //

// fix the uninteresting case

methods {
    balanceOf(address) returns uint256 envfree
}

rule transfer(env e, address recipient, uint256 amount) {
    require e.msg.sender != recipient;

    address myBalanceBefore = balanceOf(e.msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(e, recipient, amount);

    address myBalanceAfter = balanceOf(e.msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// ----- //