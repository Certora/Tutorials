// erc20 methods
methods {
    balanceOf(address)                    returns (uint256) envfree
    transfer(address,uint256)             returns (bool)

    allowance(address,address)            returns (uint256) envfree
    transferFrom(address,address,uint256) returns (bool)
    approve(address,uint256)              returns (bool)
}

// Calling `transfer(recipient, amount)` results in `balanceOf(msg.sender)` 
// decreasing by `amount` and `balanceOf(recipient)` increasing by `amount`
rule transferSpec(env e, address recipient, uint256 amount) {
    require e.msg.sender != recipient;

    uint256 myBalance = balanceOf(e.msg.sender);
    uint256 recipientBalance = balanceOf(recipient);

    transfer(e, recipient, amount);

    uint256 myBalanceAfter = balanceOf(e.msg.sender);
    uint256 recipientBalanceAfter = balanceOf(recipient);

    assert myBalanceAfter == myBalance - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}
/// link https://vaas-stg.certora.com/output/93493/824824706862a17d548a?anonymousKey=08dc8f240c32da2c2624962fc10d4281a09d23af

// if you call transfer and you don't have the funds, the transaction reverts
rule transferReverts(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) < amount;
    transfer@withrevert(e, recipient, amount);
    assert lastReverted;
}
/// link: https://vaas-stg.certora.com/output/93493/c8fa900528b5b1aa6537/?anonymousKey=766455cd1cb21286a342a4155ec16b419ba2d99e

// transfering to recipient should always result in their balance increasing
rule checkAddition(env e, address recipient, uint256 amount) {
    require recipient != e.msg.sender;

    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);

    assert amount > 0 <=> balanceAfter > balanceBefore;
}
/// link: https://vaas-stg.certora.com/output/93493/21e78521f584e34c6a15/?anonymousKey=cc03b75f69edda25037066149f0d97dea21c5de1

rule checkAdditionOfTransfer(env e, address recipient, uint256 amount) {
    uint256 balanceBefore = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfter = balanceOf(recipient);
    
    assert balanceAfter > balanceBefore;
}


// if you call transfer and do have enough funds, the transaction doesn't revert
rule transferDoesntRevert(env e, address recipient, uint256 amount) {
    require balanceOf(e.msg.sender) > amount;
    require e.msg.value == 0;
    require balanceOf(recipient) + amount < max_uint;
    require e.msg.sender != 0;
    require recipient != 0;

    transfer@withrevert(e, recipient, amount);
    assert !lastReverted;
}
// link: https://vaas-stg.certora.com/output/93493/cad31dda9c62bb4b21b3/?anonymousKey=e8077ac0a4a4a5971fbf534aa887cb522df1d2db


/**** Exercises ****/

/// if you call transferFrom and the transaction doesn't revert, your balance decreases and recipient's balance increases
rule transferFromSpec(env e, address recipient, uint256 amount) {
    assert false;
}

/// if you call transferFrom and you don't have the funds, the transaction reverts
rule transferFromReverts(env e, address recipient, uint256 amount) {
    assert false;
}

/// if you call transferFrom and do have enough funds, the transaction doesn't revert
rule transferFromDoesntRevert(env e, address recipient, uint256 amount) {
    assert false;
}




/**** Parametric examples ****/

/// The caller of `approve` must be the owner of the tokens involved.

rule onlyOwnerCanApprove {
    env e;
    address owner;
    address spender;
    uint256 amount;

    uint256 allowanceBefore = allowance(owner, spender);

    approve(e, spender, amount);

    uint256 allowanceAfter = allowance(owner, spender);

    assert allowanceBefore != allowanceAfter => owner == e.msg.sender,
        "The caller of `approve` must be the owner of the tokens involved";
}

/// The caller of a function which changes an allowance must be the owner of the tokens involved.

rule onlyOwnerCanChangeAllowance {
    method f;
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);

    assert allowanceBefore != allowanceAfter => owner == e.msg.sender,
        "The caller of a function which changes an allowance must be the owner 
        of the tokens involved";
}

/// The caller of a function which increases an allowance must be the owner of the tokens involved.

rule onlyOwnerCanIncreaseAllowance {
    method f;
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);

    assert allowanceBefore < allowanceAfter => owner == e.msg.sender,
        "The caller of a function which increases an allowance must be the 
        owner of the tokens involved";
}


/// A user's allowance must change only as a result of calls to `approve`, `transferFrom`, `increaseAllowance` or `decreaseAllowance`.

rule onlyCertainMethodsChangeAllowances {
    method f;
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);    

    assert allowanceBefore != allowanceAfter => 
        (f.selector == approve(address, uint256).selector ||
         f.selector == transferFrom(address, address, uint256).selector ||
         f.selector == increaseAllowance(address, uint256).selector ||
         f.selector == decreaseAllowance(address, uint256).selector),
         "A user's allowance must change only as a result of calls to 
         `approve`, `transferFrom`, `increaseAllowance` or `decreaseAllowance`";
}

/// Without a call to `approve`, `transferFrom`, `increaseAllowance` or `decreaseAllowance`, a user's allowance must not change.

rule withoutCertainMethodsAllowancesDontChange(method f)
filtered {
    f -> f.selector != approve(address, uint).selector
      && f.selector != transferFrom(address, address, uint256).selector
      && f.selector != increaseAllowance(address, uint256).selector
      && f.selector != decreaseAllowance(address, uint256).selector
}
{
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);    

    assert allowanceBefore == allowanceAfter,
        "Without a call to `approve`, `transferFrom`, `increaseAllowance` or 
        `decreaseAllowance`, a user's allowance must not change";
}

/**** Exercises ****/

/// We have been considering the question: If there is a change in `allowance`, 
/// what else must necessarily be the case?

/// Now consider the question: If there is a change in token balance, what else 
/// must necessarily be the case?

/// Using what we’ve learned, write some parametric rules to test whether the 
/// contract is functioning as it should.


