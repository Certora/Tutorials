methods {
    getLength()                 returns (uint)      envfree
    getArrSum()                 returns (uint)      envfree
}

ghost uint256 ghostArrSum
{
    init_state axiom ghostArrSum == 0;
}
ghost uint256 StartGhostArrLength;

ghost mapping(uint256 => uint256) validInternalIndexes;
ghost mapping(uint256 => uint256) reverseValidInternalIndexes;
ghost uint256 lengthOfValidInternalIndexes;

hook Sload uint256 val arr[INDEX uint256 index] STORAGE {
    uint256 shortcutIndex = reverseValidInternalIndexes[index];
    bool firstAccess = (index >= StartGhostArrLength) && ((shortcutIndex >= lengthOfValidInternalIndexes) || validInternalIndexes[shortcutIndex] != index);
    reverseValidInternalIndexes[index] = firstAccess?lengthOfValidInternalIndexes:reverseValidInternalIndexes[index];
    validInternalIndexes[lengthOfValidInternalIndexes] = index;
    lengthOfValidInternalIndexes = lengthOfValidInternalIndexes + to_uint256(firstAccess?1:0);
    uint256 val_eff = firstAccess? val:0;
    ghostArrSum = ghostArrSum + val_eff;
}

hook Sstore arr[INDEX uint256 index] uint256 new_val (uint256 old_val) STORAGE
{
    uint256 shortcutIndex = reverseValidInternalIndexes[index];
    bool firstAccess = (index >= StartGhostArrLength) && ((shortcutIndex >= lengthOfValidInternalIndexes) || validInternalIndexes[shortcutIndex] != index);
    reverseValidInternalIndexes[index] = firstAccess?lengthOfValidInternalIndexes:reverseValidInternalIndexes[index];
    validInternalIndexes[lengthOfValidInternalIndexes] = index;
    lengthOfValidInternalIndexes = lengthOfValidInternalIndexes + to_uint256(firstAccess?1:0);
    uint256 old_val_eff = firstAccess? 0:old_val;

    ghostArrSum = ghostArrSum + new_val - old_val_eff;
}

invariant sumGhostWork()
    getArrSum() == ghostArrSum
    {
        preserved{
            require StartGhostArrLength == getLength();
            require lengthOfValidInternalIndexes == 0;
        }
    }
