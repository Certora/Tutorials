# Learn How To Run The Prover Using A configuration file

## Using command line

Let's recap the basic structure of the `certoraRun` command:

- It starts with the command `certoraRun`.

- Right after we specify the relative path to the solidity file that holds the contract we'd like to verify - `<relative/path/to/solidity/file>` (meaning relative to the current working directory).

- Next, we write the contract we desire to verify, separated from the solidity file path by full colon - `:<contract_name>`. We do it since a single solidity file can contain multiple contracts.

- Right after we use the flag `--verify` to indicate that we'd like to verify the specified contract within the specified `.sol` file.

- We then specify the contract we'd like to specify again to avoid ambiguity, followed by full colon - `<contract_name>:`.

- After we specify the contract we'd like to verify again, we need to specify the `spec` file according to which we want to verify the contract - `<relative/path/to/spec/file>`

At the end the run command should look something like that (assuming our current working directory
is `01.Lesson_GettingStarted/`):

```CVL
certoraRun ERC20Lesson1/ERC20.sol:ERC20 --verify ERC20:ERC20Lesson1/Parametric.spec
```

## Using a configuration file

- [ ] Open the config file [verifyERC20](verifyERC20.conf) and read it. The format used is
  [JSON5](https://json5.org/). Make sure that you understand all fields and the
  data they require.

- [ ] In general, to use a config file, simply enter: `certoraRun <path to config file>`

> :bulb: If using relative paths in the config file, they should be relative to the
  current working directory where you enter `certoraRun`.

</br>

> :bulb: Remember, you can use `certoraRun --help` command to read more about the flags and the run command syntax.

</br>

- [ ] In your VSCode terminal change directory to `01.Lesson_GettingStarted/ERC20Lesson1/`,
  and execute the command 

```bash
certoraRun ../RunConfExample/verifyERC20.conf
```

> :memo: You can check the verification report to see that it really is the same run.

</br>

---

## Exercise

</br>

> :warning: For the following exercise make sure that you have the mentioned solidity compilers on your pc, and in the same directory that was added to the PATH during installation.

</br>

- [ ] Create a config that runs the entire `TotalGreaterThanUser.spec` specification file with solidity compiler 8.0 and a message string "My first Certora conf".
  Save the config in `RunConfExample` folder with the name `myOwnVerificationConf.conf` and run it.

</br>

- [ ] Change the contract name from ERC20 to NewERC20 (without changing the file name) and create a config that runs `TotalGreaterThanUser.spec` specification file with solidity compiler 8.0.
  Modify the previously created config file accordingly and verify that it still runs.

 </br>

 > :bulb: If you were checking the call trace in each of the runs you made, you may have noticed that the counter examples supplied by the Prover are distinct in each run.
