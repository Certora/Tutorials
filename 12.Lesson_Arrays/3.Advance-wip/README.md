## 3. Advanced - WIP 
In [ArrayWithMap.sol](ArrayWithMap.sol) we have the `ArrayWithMap` contract.
There, the contract uses a mapping to indicate which addresses inhabit the array.
We will learn here how to write invariants for this type of implementation using ghosts.
Note that `ArrayWithMap` has additional interface functions such as `set` and `swap`.

The file [ArrayWithMap.spec](ArrayWithMap.spec) contains the skeleton of a
specification file. Use ghosts and additional invariants and rules to fix the spec.


<details>
<summary>Hints.</summary>

1. To prove `uniqueArray`, it suffices to require `flagConsistency`.
1. Create a ghost mapping that provides an inverse to `get(i)`.

</details>
