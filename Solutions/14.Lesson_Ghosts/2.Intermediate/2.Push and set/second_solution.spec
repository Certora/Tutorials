methods {
    getArrSum()                 returns (uint)      envfree
    getLength() envfree
    get(uint) returns (uint)
    pushThenChangeValue(uint) envfree
}
ghost uint256 ghostArrSum
{
    init_state axiom ghostArrSum == 0;
}
ghost bool pushAndChangedCalled  {
    init_state axiom pushAndChangedCalled == false;
}
ghost uint256 arrayLength
{
    init_state axiom arrayLength == 0;
}
hook Sload uint256 val arr[INDEX uint256 index] STORAGE 
{
    require true;
}
hook Sstore arr[INDEX uint256 index] uint256 new_val (uint256 old_val) STORAGE
{
     ghostArrSum = index < arrayLength ?
        ghostArrSum + new_val - old_val :
        ghostArrSum + new_val;
    arrayLength = pushAndChangedCalled ?
    arrayLength + 1 : arrayLength;
}
invariant sumGhostWork()
    getArrSum() == ghostArrSum
    {
        preserved {
            require getLength() == arrayLength;
        }
        preserved pushThenChangeValue(uint x) {
            require getLength() == arrayLength;
            require pushAndChangedCalled;
        }
    }

