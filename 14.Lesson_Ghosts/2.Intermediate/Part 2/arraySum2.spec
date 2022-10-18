methods {
    getArrSum()                 returns (uint)      envfree
}

ghost uint256 ghostArrSum
{
    init_state axiom ghostArrSum == 0;
}

hook Sload uint256 val arr[INDEX uint256 index] STORAGE 
{
    require true;
}

hook Sstore arr[INDEX uint256 index] uint256 new_val (uint256 old_val) STORAGE
{
    require true;
}

invariant sumGhostWork()
    getArrSum() == ghostArrSum

