# Installation, Setups and Hello Certora

## Software Installations

</br>

- [ ] Follow the installation instructions for the Certora Prover described in the following link: [Installation of Certora Prover](https://docs.certora.com/en/latest/docs/user-guide/getting-started/install.html#).

> :warning: Make sure to download solidity compiler versions 0.8.7, 0.8.0, 0.7.6, 0.7.5 and 0.7.0 for the first 2 lessons of the course. You will need additional solc versions in the future; so whenever a solc error will rise, make sure to have the compiler version that you need on your local machine, located in a directory added to PATH.

</br>

- [ ] Install VSCode if you don't already have it (can be found in their [official website](https://code.visualstudio.com/)).

</br>

- [ ] In the VSCode extensions/marketplace search for [Certora Verification Language LSP](https://marketplace.visualstudio.com/items?itemName=Certora.evmspec-lsp) and install it. This is an extension developed for supporting the spec language - the language in which we will be writing specifications. The extension supports syntax highlighting, autocompletion and more.

- [ ] It is also recommended to install the [Ethereum Security Bundle](https://marketplace.visualstudio.com/items?itemName=tintinweb.ethereum-security-bundle) by tintinweb on the VSCode extensions/marketplace, to get support for the Solidity contracts.

</br>

---

## Course Setup

</br>

- [ ] Fork the [Tutorials](https://github.com/Certora/Tutorials) repository to your github account. </br>
You can use the following link as a guide: [Forking Repository On Github](https://docs.github.com/en/get-started/quickstart/fork-a-repo#forking-a-repository). </br>
Clone your repository to your local machine so you'll have everything you need on your pc.

</br>

- [ ] Make sure to sync the forked repository daily in case any changes and fixes were made to the original repository. Use this link as a guide: [Syncing A Forked Repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo#configuring-git-to-sync-your-fork-with-the-original-repository).

</br>

- [ ] Register to our [Discourse Forum](https://forum.certora.com/) and consider and introduce yourself in the [Introduction Thread](https://forum.certora.com/t/introduce-yourself/27/2).

</br>

---

## Certora Prover Basic

</br>

> :information_source: The Certora team recommends using VSCode as your main editor for writing specifications and browsing through contracts during the course. As part of the everyday work, you'll need convenient access to terminal, .spec editor - preferably with SLP extension, and a solidity editor - preferably with extension that has adequate support for reading and writing solidity code.
You may, however, choose to work with any other (textual) editor of your choice or split the work between several editors, just know that the SLP is currently only supported through VSCode.

</br>

- [ ] Follow the [ERC20Lesson1](ERC20Lesson1) instructions to learn the basics of operating the Certora Prover.

</br>

- [ ] Watch a lecture presented at Stanford Aug 2022 team by Dr. Michael George - [Link](`https://www.youtube.com/watch?v=siEDkMNbl5o). The lecture goes over the same examples from ERC20, explaining core concepts in more detail.

</br>

---

## Running the Prover Using Configuration Files

</br>

For larger projects, the command line for running the Certora Prover can become large
and cumbersome. It is therefore recommended to use _configuration files_ instead.
These are [JSON5](https://json5.org/) files (with ".conf" extension) that hold the
parameters and options for the Certora Prover. Here is an example conf file:

```json5
{
    "files": [
        "src/contracts/Strategy.sol",
        "src/contracts/Data.sol",
    ],
    "verify": "Strategy:certora/specs/StrategyVrification.spec",
    "send_only": false,
    "optimistic_loop": true,
    "loop_iter": "2",
    "rule_sanity": "basic",
    // Note: json5 supports comments!
    "solc": "solc8.8",
    "msg": "Strategy verification"
}
```

Now running the Certora Prover is simply entering 
```bash
certoraRun config_file.conf
```

There are other reasons to prefer configuration files over directly using CLI:
1. They are easier to read and sometimes can be more friendly to edit.
2. Since the configuration files are [JSON5](https://json5.org/), they support comments.
3. We can include them in our git repository for version control.


</br>

- [ ] Follow the instructions on [RunScriptExample](RunScriptExample) to learn how to
  write run scripts, and how to execute the prover using scripts.

</br>

---

## Understanding Violations and Following Counter Examples

</br>

- [ ] Continue to the next lesson: [Investigate Violations](../02.Lesson_InvestigateViolations) to exercise some more script writing and the art of understanding violations.

</br>

---
## Solutions to the lessons

</br>

- [ ] Some of the lessons in the Tutorials require you to write a `.spec` file containing your own rules for a given contract. Sometimes this can be quite challenging and if you get in trouble, you can have a look at the [Solutions](https://github.com/Certora/Tutorials/tree/master/Solutions) folder in the repository.

</br>

---

### Hurray! You've completed your first step toward being a security engineer

---
