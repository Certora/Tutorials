methods {
    set(uint, address)                              envfree
    push(address)                                   envfree
    pop()                                           envfree
    removeReplaceFromEnd(uint)                      envfree
    get(uint)                   returns (address)   envfree
    getWithDefaultValue(uint)   returns (address)   envfree
    getArr()                    returns (address[]) envfree
    getLength()                 returns (uint)      envfree
    frequency(address)          returns (uint)      envfree
}

 ghost mapping(uint => address) arrOfTokensMirror {
    init_state axiom forall uint i. arrOfTokensMirror[i]==0;
 }
 ghost length() returns uint256{
    init_state axiom length()==0;
 }




hook Sstore arrOfTokens[INDEX uint256 index] address newValue (address oldValue) STORAGE 
{
	// Here you can update your ghosts whenever arrOfTokens is updated
    arrOfTokensMirror[index] =  newValue;
    havoc length assuming length@new() > index;
}
// Use this hook to update ghosts whenever arrOfTokens is read
hook Sload address value arrOfTokens[INDEX uint256 index] STORAGE 
{
    require arrOfTokensMirror[index] ==  value;
    require length() > index;
}

invariant uniqueArray() 
    forall uint256 i. forall uint256 j. 
         (i < length() && j < length() && i!= j ) => (
        (arrOfTokensMirror[i] != arrOfTokensMirror[j]) ||
		((arrOfTokensMirror[i] == 0) && (arrOfTokensMirror[j] == 0)))


rule simpleAsThat() {
    address x;
    requireInvariant uniqueArray();
    assert x!=0 => frequency(x) <= 1; 
}