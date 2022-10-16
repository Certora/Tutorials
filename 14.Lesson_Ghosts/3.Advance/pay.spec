methods{
    getOwner() returns(address) envfree
}



hook Sload bytes32 value _list .(offset 0)[INDEX uint256 index] STORAGE {
    require true;
}

hook Sstore _list .(offset 0)[INDEX uint256 index] bytes32 newValue (bytes32 oldValue) STORAGE {
    require true;
}

hook Sload uint256 index _list .(offset 32)[KEY bytes32 value] STORAGE {
    require true;
}

hook Sstore _list .(offset 32)[KEY bytes32 value] uint256 newIndex (uint256 oldIndex) STORAGE {
    require true;
}

hook Sstore _list .(offset 0).(offset 0) uint256 newLen (uint256 oldLen) STORAGE {
    require true;
}

hook Sload uint256 len _list .(offset 0).(offset 0) STORAGE {
    require true;
}




invariant ownerOnlyZero()
    getOwner() == 0

