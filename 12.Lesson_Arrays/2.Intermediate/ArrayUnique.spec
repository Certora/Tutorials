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
 ghost uint256 length;


hook Sstore arrOfTokens.(offset 0) uint256 newLen STORAGE
{
    length = newLen;
}
hook Sload uint256 theLen arrOfTokens.(offset 0) STORAGE
{
    require length == theLen;
}

hook Sstore arrOfTokens[INDEX uint256 index] address newValue (address oldValue) STORAGE 
{
	// Here you can update your ghosts whenever arrOfTokens is updated
    arrOfTokensMirror[index] =  newValue;
    assert length > index;
}
// Use this hook to update ghosts whenever arrOfTokens is read
hook Sload address value arrOfTokens[INDEX uint256 index] STORAGE 
{
    require arrOfTokensMirror[index] ==  value;
    assert length > index;
}

invariant uniqueArray() 
    forall uint256 i. forall uint256 j. 
         (i < length && j < length && i!= j ) => (
        (arrOfTokensMirror[i] != arrOfTokensMirror[j]) ||
		((arrOfTokensMirror[i] == 0) && (arrOfTokensMirror[j] == 0)))


rule simpleAsThat() {
    address x;
    requireInvariant uniqueArray();
    assert x!=0 => frequency(x) <= 1; 
}