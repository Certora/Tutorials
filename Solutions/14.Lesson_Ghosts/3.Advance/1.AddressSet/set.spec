/**
 * @title get Set array length
 * @dev user should define getLen() in Solidity harness file.
 */
methods{
    getLen() returns (uint256) envfree
    atIndex(uint256) returns(address) envfree
    contains(address) returns(bool) envfree
}
/**
* @title max uint256
* @retrun 2^256-1
*/
definition MAX_UINT256() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
/**
* @title max address value + 1
* @retruns 2^160
*/
definition TWO_TO_160() returns uint256 = 0x10000000000000000000000000000000000000000;


/**
* @title Set map entries point to valid array entries
* @notice an essential condition of the set, should hold for evert Set implementation 
* @return true if all map entries points to valid indexes of the array.
*/
definition MAP_POINTS_INSIDE_ARRAY_INIT(bytes32 a) returns bool = mirrorMapInit[a] <= mirrorArrayLenInit;
/**
* @title Set map is the inverse function of set array. 
* @notice an essential condition of the set, should hold for evert Set implementation 
* @notice this condition depends on the other set conditions, but the other conditions do not depend on this condition.
*          If this condition is omitted the rest of the conditions still hold, but the other conditions are required to prove this condition.
* @retrun true if for every valid index of the array it holds that map(array(index)) == index + 1.
*/
definition MAP_IS_INVERSE_OF_ARRAY_INIT(uint256 i) returns bool = (i < mirrorArrayLenInit) => (mirrorMapInit[mirrorArrayInit[i]]) == to_uint256(i + 1);

/**
* @title Set array is the inverse function of set map
* @notice an essential condition of the set, should hold for evert Set implementation 
* @return true if for every non-zero bytes32 value stored in in the set map it holds that array(map(value) - 1) == value
*/
definition ARRAY_IS_INVERSE_OF_MAP_INIT(bytes32 a) returns bool = (mirrorMapInit[a] != 0) => (mirrorArrayInit[to_uint256(mirrorMapInit[a]-1)] == a);// make sure that to_uint256(mirrorMap[a]-1) does not revert when mirrorMap[a] == 0



/**
* @title Set map entries point to valid array entries
* @notice an essential condition of the set, should hold for evert Set implementation 
* @return true if all map entries points to valid indexes of the array.
*/
definition MAP_POINTS_INSIDE_ARRAY(bytes32 a) returns bool = mirrorMap[a] <= mirrorArrayLen;
/**
* @title Set map is the inverse function of set array. 
* @notice an essential condition of the set, should hold for evert Set implementation 
* @notice this condition depends on the other set conditions, but the other conditions do not depend on this condition.
*          If this condition is omitted the rest of the conditions still hold, but the other conditions are required to prove this condition.
* @retrun true if for every valid index of the array it holds that map(array(index)) == index + 1.
*/
definition MAP_IS_INVERSE_OF_ARRAY(uint256 i) returns bool = (i < mirrorArrayLen) => (mirrorMap[mirrorArray[i]]) == to_uint256(i + 1);

/**
* @title Set array is the inverse function of set map
* @notice an essential condition of the set, should hold for evert Set implementation 
* @return true if for every non-zero bytes32 value stored in in the set map it holds that array(map(value) - 1) == value
*/
definition ARRAY_IS_INVERSE_OF_MAP(bytes32 a) returns bool = (mirrorMap[a] != 0) => (mirrorArray[to_uint256(mirrorMap[a]-1)] == a);// make sure that to_uint256(mirrorMap[a]-1) does not revert when mirrorMap[a] == 0


/**
* @title load array length
* @notice a dummy condition that forces load of array length, using it forces initialization of  mirrorArrayLen
* @return always true
*/
definition CVL_LOAD_ARRAY_LENGTH() returns bool = (getLen() == getLen());

/**
* @title Set-general condition, encapsulating all conditions of Set 
* @notice this condition recaps the general characteristics of Set. It should hold for all set implementations i.e. AddressSet, UintSet, Bytes32Set
* @retrun conjunction of the Set three essential properties.
*/
definition SET_INVARIANT(uint256 i, bytes32 a) returns bool = MAP_POINTS_INSIDE_ARRAY(a) && MAP_IS_INVERSE_OF_ARRAY(i) && ARRAY_IS_INVERSE_OF_MAP(a); 

definition SET_INVARIANT_INIT(uint256 i, bytes32 a) returns bool = MAP_POINTS_INSIDE_ARRAY_INIT(a) && MAP_IS_INVERSE_OF_ARRAY_INIT(i) && ARRAY_IS_INVERSE_OF_MAP_INIT(a); 


/**
 * @title Size of stored value does not exceed the size of an address type.
 * @notice must be used for AddressSet, must not be used for Bytes32Set, UintSet
 * @return true if all array entries are less than 160 bits.
 **/
definition VALUE_IN_BOUNDS_OF_TYPE_ADDRESS(uint256 i) returns bool = to_uint256(mirrorArray[i]) < TWO_TO_160();
definition VALUE_IN_BOUNDS_OF_TYPE_ADDRESS_INIT(uint256 i) returns bool = to_uint256(mirrorArrayInit[i]) < TWO_TO_160();

/**
 * @title A complete invariant condition for AddressSet
 * @notice invariant addressSetInvariant proves that this condition holds
 * @return conjunction of the Set-general and AddressSet-specific conditions
 **/
definition ADDRESS_SET_INVARIANT(uint256 i, bytes32 a) returns bool = SET_INVARIANT(i, a) && VALUE_IN_BOUNDS_OF_TYPE_ADDRESS(i);
definition ADDRESS_SET_INVARIANT_INIT(uint256 i, bytes32 a) returns bool = SET_INVARIANT_INIT(i, a) && VALUE_IN_BOUNDS_OF_TYPE_ADDRESS_INIT(i);

/**
 * @title A complete invariant condition for UintSet, Bytes32Set
 * @notice for UintSet and Bytes2St no type-specific condition is required because the type size is the same as the native type (bytes32) size
 * @return the Set-general condition
 **/
definition UINT_SET_INVARIANT(uint256 i, bytes32 a) returns bool = SET_INVARIANT(i, a);

/**
 * @title Out of bound array entries are zero
 * @notice A non-essential  condition. This condition can be proven as an invariant, but it is not necessary for proving the Set correctness.
 * @return true if all entries beyond array length are zero
 **/
definition ARRAY_OUT_OF_BOUND_ZERO(uint256 i) returns bool = (i >= mirrorArrayLen) => (mirrorArray[i] == 0);

// For CVL use

/**
 * @title ghost mirror map, mimics Set map
 **/
ghost mapping(bytes32=>uint256) mirrorMap{
    init_state axiom forall bytes32 a. mirrorMap[a] == 0;
}

ghost mapping(bytes32=>uint256) mirrorMapInit{
    init_state axiom forall bytes32 a. mirrorMapInit[a] == 0;
}

/**
 * @title ghost mirror array, mimics Set array
 **/
ghost mapping(uint256=>bytes32) mirrorArray{
    init_state axiom forall uint256 i. mirrorArray[i] == 0;
}

ghost mapping(uint256=>bytes32) mirrorArrayInit{
    init_state axiom forall uint256 i. mirrorArrayInit[i] == 0;
}

/**
 * @title ghost mirror array length, mimics Set array length
 * @notice ghost includes an assumption about the array length. 
  * If the assumption were not written in the ghost function it should be written in every rule and invariant.
  * The assumption holds: breaking the assumptions would violate the invariant condition 'map(array(index)) == index + 1'. Set map uses 0 as a sentinel value, so the array cannot contain MAX_INT different values.  
  * The assumption is necessary: if a value is added when length==MAX_INT then length overflows and becomes zero.
 **/
ghost uint256 mirrorArrayLen {
    init_state axiom mirrorArrayLen == 0;
    axiom mirrorArrayLen != MAX_UINT256(); 
}

ghost uint256 mirrorArrayLenInit {
    init_state axiom mirrorArrayLen == 0;
    axiom mirrorArrayLen != MAX_UINT256(); 
}


ghost bool setActive;
ghost bool addressSetActive;

ghost mapping(uint256 => uint256) validInternalIndexes;
ghost mapping(uint256 => uint256) reverseValidInternalIndexes;
ghost uint256 lengthOfValidInternalIndexes;

ghost mapping(uint256 => bytes32) validInternalIndexesMap;
ghost mapping(bytes32 => uint256) reverseValidInternalIndexesMap;
ghost uint256 lengthOfValidInternalIndexesMap;


definition ACTIVATE_SET() returns bool = (mirrorArrayLenInit == getLen()) && setActive && (lengthOfValidInternalIndexesMap == 0) && (lengthOfValidInternalIndexes == 0);
definition ACTIVATE_ADDRESS_SET() returns bool = (mirrorArrayLenInit == getLen()) && addressSetActive && (lengthOfValidInternalIndexesMap) == 0 && (lengthOfValidInternalIndexes == 0);

hook Sload bytes32 value _list .(offset 0)[INDEX uint256 index] STORAGE {
    uint256 shortcutIndex = reverseValidInternalIndexes[index];
    bool firstAccessArray = ((shortcutIndex >= lengthOfValidInternalIndexes) || validInternalIndexes[shortcutIndex] != index);
    reverseValidInternalIndexes[index] = firstAccessArray?lengthOfValidInternalIndexes:reverseValidInternalIndexes[index];
    validInternalIndexes[lengthOfValidInternalIndexes] = index;
    lengthOfValidInternalIndexes = lengthOfValidInternalIndexes + to_uint256(firstAccessArray?1:0);
    require mirrorArrayInit[index] == (firstAccessArray?value:mirrorArrayInit[index]);

    bool firstAccess = firstAccessArray;
    require firstAccess && setActive => SET_INVARIANT_INIT(index, value);
    require firstAccess && addressSetActive => ADDRESS_SET_INVARIANT_INIT(index, value);

    require mirrorArray[index] == value;
}

hook Sstore _list .(offset 0)[INDEX uint256 index] bytes32 newValue (bytes32 oldValue) STORAGE {
    uint256 shortcutIndex = reverseValidInternalIndexes[index];
    bool firstAccessArray = ((shortcutIndex >= lengthOfValidInternalIndexes) || validInternalIndexes[shortcutIndex] != index);
    reverseValidInternalIndexes[index] = firstAccessArray?lengthOfValidInternalIndexes:reverseValidInternalIndexes[index];
    validInternalIndexes[lengthOfValidInternalIndexes] = index;
    lengthOfValidInternalIndexes = lengthOfValidInternalIndexes + to_uint256(firstAccessArray?1:0);
    require mirrorArrayInit[index] == (firstAccessArray?oldValue:mirrorArrayInit[index]);

    bool firstAccess = firstAccessArray;
    require firstAccess && setActive => SET_INVARIANT_INIT(index, oldValue);
    require firstAccess && addressSetActive => ADDRESS_SET_INVARIANT_INIT(index, oldValue);

    require mirrorArray[index] == oldValue;
    mirrorArray[index] = newValue;
}



hook Sload uint256 index _list .(offset 32)[KEY bytes32 value] STORAGE {
    uint256 shortcutIndexMap = reverseValidInternalIndexesMap[value];
    bool firstAccessMap = ((shortcutIndexMap >= lengthOfValidInternalIndexesMap) || validInternalIndexesMap[shortcutIndexMap] != value);
    reverseValidInternalIndexesMap[value] = firstAccessMap?lengthOfValidInternalIndexesMap:reverseValidInternalIndexesMap[value];
    validInternalIndexesMap[lengthOfValidInternalIndexesMap] = value;
    lengthOfValidInternalIndexesMap = lengthOfValidInternalIndexesMap + to_uint256(firstAccessMap?1:0);
    require mirrorMapInit[value] == (firstAccessMap?index:mirrorMapInit[value]);

    bool firstAccess = firstAccessMap;
    require (firstAccess && setActive) => ((index != 0) => SET_INVARIANT_INIT(to_uint256(index - 1), value));
    require (firstAccess && addressSetActive) => ((index != 0) =>ADDRESS_SET_INVARIANT_INIT(to_uint256(index - 1), value));

    require mirrorMap[value] == index;
}

hook Sstore _list .(offset 32)[KEY bytes32 value] uint256 newIndex (uint256 oldIndex) STORAGE {
    uint256 shortcutIndexMap = reverseValidInternalIndexesMap[value];
    bool firstAccessMap = ((shortcutIndexMap >= lengthOfValidInternalIndexesMap) || validInternalIndexesMap[shortcutIndexMap] != value);
    reverseValidInternalIndexesMap[value] = firstAccessMap?lengthOfValidInternalIndexesMap:reverseValidInternalIndexesMap[value];
    validInternalIndexesMap[lengthOfValidInternalIndexesMap] = value;
    lengthOfValidInternalIndexesMap = lengthOfValidInternalIndexesMap + to_uint256(firstAccessMap?1:0);
    require mirrorMapInit[value] == (firstAccessMap?oldIndex:mirrorMapInit[value]);

    bool firstAccess = firstAccessMap;
    require (firstAccess && setActive) => ((oldIndex != 0) => SET_INVARIANT_INIT(to_uint256(oldIndex - 1), value));
    require (firstAccess && addressSetActive) => ((oldIndex != 0) => ADDRESS_SET_INVARIANT_INIT(to_uint256(oldIndex - 1), value));

    require mirrorMap[value] == oldIndex;
    mirrorMap[value] = newIndex;
}

/**
 * @title hook for Set array length stores
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sstore _list .(offset 0).(offset 0) uint256 newLen (uint256 oldLen) STORAGE {
    require mirrorArrayLen == oldLen;
    mirrorArrayLen = newLen;
    // havoc mirrorArrayLen assuming (mirrorArrayLen@new() == newLen && mirrorArrayLen@old() == oldLen);
}

/**
 * @title hook for Set array length load
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sload uint256 len _list .(offset 0).(offset 0) STORAGE {
    require mirrorArrayLen == len;
}

/**
 * @title main Set general invariant
 **/
invariant setInvariant(uint256 i, bytes32 a)
    SET_INVARIANT(i, a)
    {
        preserved{
            require ACTIVATE_SET();
        }
    }

// /**
//  * @title main AddressSet invariant
//  * @dev user of the spec should add 'require ACTIVATE_ADDRESS_SET();' to every rule and invariant that refer to a contract that instantiates AddressSet  
//  **/
invariant addressSetInvariant(uint256 i, address a)
    ADDRESS_SET_INVARIANT(i, a)
    {
        preserved{
            require ACTIVATE_ADDRESS_SET();
        }
    }


// /**
//  * @title addAddress() successfully adds an address
//  **/
rule api_add_succeeded()
{
    env e;
    address a;
    require ACTIVATE_ADDRESS_SET();
    require !contains(a);
    assert addAddress(e, a);
    assert contains(a);
}

/**
 * @title addAddress() fails to add an address if it already exists 
 * @notice check set membership using contains()
 **/
rule api_add_failed_contains()
{
    env e;
    address a;
    require ACTIVATE_ADDRESS_SET();
    require contains(a);
    assert !addAddress(e, a);
}

/**
 * @title addAddress() fails to add an address if it already exists 
 * @notice check set membership using atIndex()
 **/
rule api_add_failed_at()
{
    env e;
    address a;
    uint256 index;
    require ACTIVATE_ADDRESS_SET();
    require atIndex(index) == a;
    assert !addAddress(e, a);
}

/**
 * @title contains() succeed after addAddress succeeded 
 **/
rule api_address_contained_affter_add()
{
    env e;
    address a;
    require ACTIVATE_ADDRESS_SET();
    addAddress(e, a);
    assert contains(a);
}

/**
 * @title _removeAddress() succeeds to remove an address if it existed 
 * @notice check set membership using contains()
 **/
rule api_remove_succeeded_contains()
{
    env e;
    address a;
    require ACTIVATE_ADDRESS_SET();
    require contains(a);
    assert _removeAddress(e, a);
}

/**
 * @title _removeAddress() fails to remove address if it didn't exist 
 **/
rule api_remove_failed()
{
    env e;
    address a;
    require ACTIVATE_ADDRESS_SET();
    require !contains(a);
    assert !_removeAddress(e, a);
}

/**
 * @title _removeAddress() succeeds to remove an address if it existed 
 * @notice check set membership using atIndex()
 **/
rule api_remove_succeeded_at()
{
    env e;
    address a;
    uint256 index;
    require ACTIVATE_ADDRESS_SET();
    require atIndex(index) == a;
    assert _removeAddress(e, a);
}

/**
 * @title contains() failed after an address was removed
 **/
rule api_not_contains_affter_remove()
{
    env e;
    address a;
    require ACTIVATE_ADDRESS_SET();
    _removeAddress(e, a);
    assert !contains(a);
}

/**
 * @title contains() succeeds if atIndex() succeeded
 **/
rule cover_at_contains()
{
    env e;
    address a = 0;
    require ACTIVATE_ADDRESS_SET();
    uint256 index;
    require atIndex(index) == a;
    assert contains(a);
}

/**
 * @title Solidity getArrayLength() and mirror ghost variable are identical
 **/
rule api_len()
{
    require ACTIVATE_ADDRESS_SET();
    assert mirrorArrayLen == getLen();
}


/**
 * @title cover properties, checking various array lengths
 * @notice The assertion should fail - it's a cover property written as an assertion. For large length, beyond loop_iter the assertion should pass.
 **/

rule cover_len0(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 0;}
rule cover_len1(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 1;}
rule cover_len2(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 2;}
rule cover_len3(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 3;}
rule cover_len4(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 4;}
rule cover_len5(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 5;}
rule cover_len6(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 6;}
rule cover_len7(){require ACTIVATE_ADDRESS_SET();assert mirrorArrayLen != 7;}
rule cover_len8(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 8;}
rule cover_len16(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 16;}
rule cover_len32(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 32;}
rule cover_len64(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 64;}
rule cover_len128(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 128;}
rule cover_len256(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 256;}
rule cover_len512(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 512;}
rule cover_len1024(){require ACTIVATE_ADDRESS_SET(); assert mirrorArrayLen != 1024;}
