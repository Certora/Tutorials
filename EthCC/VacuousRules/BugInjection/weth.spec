
methods {
    symbol() envfree
    decimals() envfree
    balanceOf(address)
    allowance(address, address)
    deposit()
    withdraw(uint)
    totalSupply() returns (uint) envfree
    approve(address, uint) returns (bool)
    transfer(address, uint) returns (bool)
    transferFrom(address, address, uint)
}

rule depositUnitTest(env e){
    uint _balance = balanceOf(e, e.msg.sender);
    deposit(e);
    uint balance_ = balanceOf(e, e.msg.sender);
    assert balance_ == _balance + e.msg.value;
}