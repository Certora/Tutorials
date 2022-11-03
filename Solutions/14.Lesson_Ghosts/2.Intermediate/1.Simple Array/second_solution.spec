methods {
    getLength()                 returns (uint)      envfree
    getArrSum()                 returns (uint)      envfree
}
ghost mathint arrayLength {
    init_state axiom arrayLength == 0;
}
ghost uint256 ghostArrSum
{
    init_state axiom ghostArrSum == 0;
}
hook Sstore arr[INDEX uint256 index] uint256 new_val (uint256 old_val) STORAGE
{
    ghostArrSum = index < arrayLength ?
        ghostArrSum + new_val-old_val :
        ghostArrSum + new_val;
}
invariant sumGhostWork()
    getArrSum() == ghostArrSum
    {
        preserved{
            require arrayLength == getLength();
        }
    }
    
