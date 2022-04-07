methods{
    calculateFee(uint256 amount) envfree;
    getRate() returns uint256 envfree;
}

rule checkTimeout(uint256 amount){
    require(getRate()>1 && amount>20);
    assert calculateFee(amount) >= 0;

}