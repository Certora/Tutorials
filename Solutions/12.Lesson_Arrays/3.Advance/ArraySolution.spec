

methods {
    set(uint, address)                              envfree
    push(address)                                   envfree
    pop()                                           envfree
    removeReplaceFromEnd(uint)                      envfree
    get(uint)                   returns (address)   envfree
    getWithDefaultValue(uint)   returns (address)   envfree
    getArr()                    returns (address[]) envfree
    getLength()                 returns (uint)      envfree
    getFlag(address)            returns (bool)      envfree
}


ghost mapping(uint256 => address) indexSetArrayFlag;
ghost mapping(address => uint256) indexSetShortcutFlag;
ghost mapping(address => bool) mirrorInitFlag;
ghost uint256 setLengthFlag;
ghost bool Concistant_flag;

ghost mapping(uint256 => uint256) indexSetArray;
ghost mapping(uint256 => uint256) indexSetShortcut;
ghost mapping(address => uint256) reverseMapInit;
ghost uint256 setLength;
ghost bool OneToOne_arrOfTokens;




hook Sstore arrOfTokens[INDEX uint256 index] address newValue (address oldValue) STORAGE {

    // this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcut[index];
    bool firstAccess = (shortcutIndex >= setLength) || indexSetArray[shortcutIndex] != index;
    indexSetShortcut[index] = firstAccess?setLength:indexSetShortcut[index];
    indexSetArray[setLength] = index;
    setLength = setLength + (firstAccess?to_uint256(1):to_uint256(0));
    require (OneToOne_arrOfTokens && firstAccess) => (reverseMapInit[oldValue] == index);
    //end

    require (Concistant_flag && firstAccess) => (mirrorInitFlag[oldValue]);
    }
hook Sload address value arrOfTokens[INDEX uint256 index] STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcut[index];
    bool firstAccess = (shortcutIndex >= setLength) || indexSetArray[shortcutIndex] != index;
    indexSetShortcut[index] = firstAccess?setLength:indexSetShortcut[index];
    indexSetArray[setLength] = index;
    setLength = setLength + (firstAccess?to_uint256(1):to_uint256(0));
    require (OneToOne_arrOfTokens && firstAccess) => (reverseMapInit[value] == index);
    //end

    require (Concistant_flag && firstAccess) => (mirrorInitFlag[value]);
}


hook Sstore flag[KEY address a] bool newValue (bool oldValue) STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcutFlag[a];
    bool firstAccess = (shortcutIndex >= setLengthFlag) || indexSetArrayFlag[shortcutIndex] != a;
    indexSetShortcutFlag[a] = firstAccess?setLengthFlag:indexSetShortcutFlag[a];
    indexSetArrayFlag[setLengthFlag] = a;
    setLengthFlag = setLengthFlag + (firstAccess?to_uint256(1):to_uint256(0));
    require firstAccess => (mirrorInitFlag[a] == oldValue);
    //end

    }
hook Sload bool value flag[KEY address a] STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcutFlag[a];
    bool firstAccess = (shortcutIndex >= setLengthFlag) || indexSetArrayFlag[shortcutIndex] != a;
    indexSetShortcutFlag[a] = firstAccess?setLengthFlag:indexSetShortcutFlag[a];
    indexSetArrayFlag[setLengthFlag] = a;
    setLengthFlag = setLengthFlag + (firstAccess?to_uint256(1):to_uint256(0));
    require firstAccess => (mirrorInitFlag[a] == value);
    //end
}

invariant flagConsistancy(uint256 i)
    i < getLength() => getFlag(getWithDefaultValue(i))
    {
        preserved{
            require OneToOne_arrOfTokens && (setLength == 0);
            require Concistant_flag && setLengthFlag == 0;
        }
    }

invariant uniqueArray(uint256 i, uint256 j)
    i != j => ((getWithDefaultValue(i) != getWithDefaultValue(j)) || ((getWithDefaultValue(i) == 0) && (getWithDefaultValue(j) == 0)))
    {
        preserved{
            require OneToOne_arrOfTokens && (setLength == 0);
            require Concistant_flag && setLengthFlag == 0;
        }
    }
