# Learn How To Run The Prover Using A Script

</br>

Let's recap on the basic structure of the `certoraRun` command:

- It starts with the basic command `certoraRun`.

- Right after we specify the relative path to the solidity file that holds the contract we'd like to verify - `<relative/path/to/solidity/file>`.

- Next we write the contract we desire to verify, separated from the solidity file path by full colon - `:<contract_name>`. We do it since a single solidity file can contain multiple contracts.

- Right after we use the flag `--verify` to indicate that we'd like to verify the specified contract within the specified `.sol` file.

- We then specify the contract we'd like to specify again to avoid ambiguity, followed by full colon - `<contract_name>:`.

- After we specify the contract we'd like to verify again, we need to specify the `spec` file according to which we want to verify the contract - `<relative/path/to/spec/file>`

At the end the run command should look something like that:

```CVL
certoraRun BankLesson1/Bank.sol:Bank --verify Bank:BankLesson1/IntegrityOfDeposit.spec
```

</br>

- [ ] Open the shell script [verifyIntegrityOfDeposit](verifyIntegrityOfDeposit.sh) and read it. Make sure that you understand each line, and that you are familiar with every flag.

    - [ ] Do you recognize this run command? This is basically the first run in BankLesson1.

</br>

> :bulb: Remember, you can use `certoraRun --help` command to read more about the flags and the run command syntax.

</br>

- [ ] In your VSCode terminal change directory to `Certora-OnBoarding/01.Lesson_GettinStarted`, and execute the script: 

``` sh
sh  RunScriptExample/verifyIntegrityOfDeposit.sh "This is a run executed through a shell script"
```

> :memo: You can check the verification report to see that it really is the same run.

</br>

---

## Exercise:

</br>

> :warning: For the following exercise make sure that you have the mentioned solidity compilers on your pc, and in the same directory that was added to the PATH during installation.

</br>

 - [ ] Create a script that runs the entire `TotalGreaterThanUser.spec` specification file with solidity compiler 7.5 and a message string "My first Certora shell script". Save the script in `RunScriptExample` with the name "myOwnVerificationScript1" and execute the script.

</br>

 - [ ] Create a script that runs the rule `validityOfTotalFundsWithVars` in `Parametric.spec` specification file with solidity compiler 7.0 and a message of your choice taken as an input. Save the script in `RunScriptExample` with the name "myOwnVerificationScript2" and execute the script.
 
 </br>

 > :bulb: If you were checking the call trace in each of the runs you made, you may have noticed that the counter examples supplied by the prover are distinct in each run.