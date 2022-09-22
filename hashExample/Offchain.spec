methods {
  example(bytes32, bytes) returns (uint256) envfree;
  exampleViolated(bytes32, bytes) returns (uint256) envfree;
  witnessLength(bytes) returns (uint256) envfree;
}



//  Rule to test whether the example function returns only one value for a given target
//  PASSED
rule uniqueReturnVal() {
	bytes32 target;
	bytes witness1;
	bytes witness2;
	uint res1;
	uint res2;
	uint length1;
	uint length2;

	length1 = witnessLength(witness1);
	length2 = witnessLength(witness2);
	
	require length1 >0 && length1 %32 == 0 && length1 < 12*32;
	require length2 >0 && length2 %32 == 0 && length2 < 12*32;

	res1 = example(target, witness1);
	
	res2 = example(target, witness2);
	
	assert res1 == res2,"function should return only one value for a given target";
}

//  Rule to test whether the exampleViolated function returns only one value for a given target
//  VIOLATED
rule uniqueReturnValExampleViolated() {
	bytes32 target;
	bytes witness1;
	bytes witness2;
	uint res1;
	uint res2;
	uint length1;
	uint length2;

	length1 = witnessLength(witness1);
	length2 = witnessLength(witness2);
	
	require length1 >0 && length1 %32 == 0 && length1 < 12*32;
	require length2 >0 && length2 %32 == 0 && length2 < 12*32;

	res1 = exampleViolated(target, witness1);
	
	res2 = exampleViolated(target, witness2);
	
	assert res1 == res2,"function should return only one value for a given target";
}

// // Rule to verify that, for a given target, if the example function retuns a value for one witness then it must revert for a second witness
// rule revertForSecondWitness(){
// 	bytes32 target;
// 	bytes witness1;
// 	bytes witness2;
// 	uint res1;
// 	uint res2;
// 	bool revert1;
// 	bool revert2;
// 	uint length1;
// 	uint length2;

// 	require witness1 != witness2;
	
// 	length1 = witnessLength(witness1);
// 	length2 = witnessLength(witness2);
	
// 	require length1 >0 && length1 %32 == 0 && length1 < 12*32;
// 	require length2 >0 && length2 %32 == 0 && length2 < 12*32;

// 	res1 = example@withrevert(target, witness1);
// 	revert1 = lastReverted;
	
// 	res2 = example@withrevert(target, witness2);
// 	revert2 = lastReverted;

// 	assert !revert1 => revert2,"For a given target, If the function returns a value for one witness then it must revert for another witness";
// }

// // Rule to verify that, for a given target, if the exampleViolated function retuns a value for one witness then it must revert for a second witness
// rule revertForSecondWitnessExampleViolated(){
// 	bytes32 target;
// 	bytes witness1;
// 	bytes witness2;
// 	uint res1;
// 	uint res2;
// 	bool revert1;
// 	bool revert2;
// 	uint length1;
// 	uint length2;

// 	require witness1 != witness2;

// 	length1 = witnessLength(witness1);
// 	length2 = witnessLength(witness2);
	
// 	require length1 >0 && length1 %32 == 0 && length1 < 12*32;
// 	require length2 >0 && length2 %32 == 0 && length2 < 12*32;

// 	res1 = exampleViolated@withrevert(target, witness1);
// 	revert1 = lastReverted;
	
// 	res2 = exampleViolated@withrevert(target, witness2);
// 	revert2 = lastReverted;

// 	assert !revert1 => revert2,"For a given target, If the function returns a value for one witness then it must revert for another witness";
// }