// Calling `transfer(recipient, amount)` results in `balanceOf(msg.sender)` 
// decreasing by `amount` and `balanceOf(recipient)` increasing by `amount`

// -- Step-1 -- //

// want to do this, what are these random variables?
rule transferSpec {
    transfer(recipient, amount);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-2 -- //

// defined the variables, but how do we know what the other variables are?
rule transferSpec {
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
rule transferSpec(address msg.sender, address recipient, uint256 amount) {
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
rule transferSpec {
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
rule transferSpec(env e, address recipient, uint256 amount) {
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
rule transferSpec(env e, env e1, env e2, env e3, env e4, address recipient, uint256 amount) {
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
/// link https://vaas-stg.certora.com/output/93493/1ff00d81d71e881cd6da?anonymousKey=291e8910cc73e67443e9f9c285d4dcc9682e4e53
methods {
    balanceOf(address) returns uint256 envfree
}

rule transferSpec(env e, address recipient, uint256 amount) {
    uint256 myBalance = balanceOf(e.msg.sender);
    uint256 recipientBalance = balanceOf(recipient);

    transfer(e, recipient, amount);

    uint256 myBalanceAfter = balanceOf(e.msg.sender);
    uint256 recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalance - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// -- Step-8 -- //

// fix the uninteresting case of e.msg.sender == recipient
methods {
    balanceOf(address) returns uint256 envfree
}

rule transferSpec(env e, address recipient, uint256 amount) {
    require e.msg.sender != recipient;

    address myBalanceBefore = balanceOf(e.msg.sender);
    address recipientBalanceBefore = balanceOf(recipient);

    transfer(e, recipient, amount);

    address myBalanceAfter = balanceOf(e.msg.sender);
    address recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalanceBefore - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}


// ------------------------------------------------------------------ //

// transfering to recipient should always result in their balance increasing

// -- Step-1 -- //

// want to say this but need to assume amount > 0
/// link: https://prover.certora.com/output/93493/8b5cf1e2c52327e64c37?anonymousKey=35760eb3dc8290d9bafc9fb6a07471223ca81848
rule checkAdditionOfTransfer(env e, address recipient, uint256 amount) {
    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    assert balanceAfter > balanceBefore;
}

// -- Step-2 -- //

// one way is by using if else
rule checkAdditionOfTransfer(env e, address recipient, uint256 amount) {

    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    if (amount > 0) {
        assert balanceAfter > balanceBefore;
    } else {
        assert true;
    }
}

// -- Step-3 -- //

// another is by using require
rule checkAddition(env e, address recipient, uint256 amount) {
    require amount > 0;

    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    assert balanceAfter > balanceBefore;
}

// -- Step-4 -- //

// recommended way is to use an implication
/// link: https://vaas-stg.certora.com/output/93493/77e5621c6416784dab65/?anonymousKey=8cc71c985b93b1fc4e938d412dd4ec11b477a627
rule checkAddition(env e, address recipient, uint256 amount) {
    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    assert amount > 0 => balanceAfter > balanceBefore;
}

// -- Step-5 -- //

// missing one little assumption
/// link: https://vaas-stg.certora.com/output/93493/fc4dcbd6d0d8467b07b9?anonymousKey=007ab11f8fdbf7ff50b4745b025d51401127fd40
rule checkAddition(env e, address recipient, uint256 amount) {
    require recipient != e.msg.sender;

    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    assert amount > 0 => balanceAfter > balanceBefore;
}

// -- Step-6 -- //

// can make bi-implications in the assert 
/// link: https://vaas-stg.certora.com/output/93493/21e78521f584e34c6a15/?anonymousKey=cc03b75f69edda25037066149f0d97dea21c5de1
rule checkAddition(env e, address recipient, uint256 amount) {
    require recipient != e.msg.sender;

    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    assert amount > 0 <=> balanceAfter > balanceBefore;
}


// ------------------------------------------------------------------ //

// if you call transfer and do have enough funds, the transaction doesn't revert

// -- Step-1 -- //

// have enough balance, still reverts because of msg.value > 0 and non-payable function
/// link: https://vaas-stg.certora.com/output/93493/c50effc27cb05751bba8?anonymousKey=0fb67e37162faa0d78141db49cb961e101396dc0
rule transferDoesntRevert(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// -- Step-2 -- //

// reverts because of overflow
/// link: https://vaas-stg.certora.com/output/93493/6f01654f7ff1d4d48a54/?anonymousKey=3a6306692c778fddb5d3e32da346a9dd0eb071cd
rule transferDoesntRevert1(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// -- Step-3 -- //

// revert reason: sending to 0 address
// link: https://vaas-stg.certora.com/output/93493/b27ededc5b996dfcadea?anonymousKey=1c5156807322eb08b09c043b5c5de0d60307bc19
rule transferDoesntRevert2(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// -- Step-4 -- //

// revert reason: sending from 0 address
/// link: https://vaas-stg.certora.com/output/93493/bf639a4e5d332e1d7853/?anonymousKey=d15b8038eb4d208d07fd2f7fc0cbb6f4dc4f0c5a
rule transferDoesntRevert3(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require e.msg.sender != 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

// -- Step-5 -- //

// works
/// link: https://vaas-stg.certora.com/output/93493/cad31dda9c62bb4b21b3/?anonymousKey=e8077ac0a4a4a5971fbf534aa887cb522df1d2db
rule transferDoesntRevert(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require e.msg.sender != 0;
    require recipient != 0;
    
    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}

