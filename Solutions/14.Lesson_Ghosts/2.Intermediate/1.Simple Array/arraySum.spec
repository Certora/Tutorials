methods {
    getLength()                 returns (uint)      envfree
    getArrSum()                 returns (uint)      envfree
}

ghost uint256 ghostArrSum
{
    init_state axiom ghostArrSum == 0;
}
ghost uint256 StartGhostArrLength;

hook Sstore arr[INDEX uint256 index] uint256 new_val (uint256 old_val) STORAGE
{
    bool firstAccess = index >= StartGhostArrLength;
    uint256 old_val_eff = firstAccess? 0:old_val;
    ghostArrSum = ghostArrSum + new_val - old_val_eff;
}

invariant sumGhostWork()
    getArrSum() == ghostArrSum
    {
        preserved{
            require StartGhostArrLength == getLength();
        }
    }
