# Installation, Setups and Hello Certora

## Software Installations

</br>

- [x] Follow the installation instructions for the Certora Prover described in the following link: [Installation of Certora Prover](https://docs.certora.com/en/latest/docs/user-guide/getting-started/install.html#).

> :warning: Make sure to download solidity compiler versions 0.8.7, 0.8.0, 0.7.6, 0.7.5 and 0.7.0 for the first 2 lessons of the course. You will need additional solc versions in the future; so whenever a solc error will rise, make sure to have the compiler version that you need on your local machine, located in a directory added to PATH.

</br>

- [x] Install VSCode if you don't already have it (can be found in their [official website](https://code.visualstudio.com/)).

</br>

- [x] In the VSCode extensions/marketplace search for [Certora Verification Language LSP](https://marketplace.visualstudio.com/items?itemName=Certora.evmspec-lsp) and install it. This is an extension developed for supporting the spec language - the language in which we will be writing specifications. The extension supports syntax highlighting, autocompletion and more.

- [x] It is also recommended to install the [Ethereum Security Bundle](https://marketplace.visualstudio.com/items?itemName=tintinweb.ethereum-security-bundle) by tintinweb on the VSCode extensions/marketplace, to get support for the Solidity contracts.

</br>

---

## Course Setup

</br>

- [x] Fork the [Tutorials](https://github.com/Certora/Tutorials) repository to your github account. </br>
You can use the following link as a guide: [Forking Repository On Github](https://docs.github.com/en/get-started/quickstart/fork-a-repo#forking-a-repository). </br>
Clone your repository to your local machine so you'll have everything you need on your pc.

</br>

- [x] Make sure to sync the forked repository daily in case any changes and fixes were made to the original repository. Use this link as a guide: [Syncing A Forked Repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo#configuring-git-to-sync-your-fork-with-the-original-repository).

</br>

- [x] Register to our [Discourse Forum](https://forum.certora.com/) and consider to introduce yourself in the [Introduction Thread](https://forum.certora.com/t/introduce-yourself/27/2).

</br>

---

## Certora Prover Basic

</br>

> :information_source: The Certora team's recommends using VSCode as your main editor for writing specifications and browsing through contracts during the course. As part of the everyday work, you'll need convenient access to terminal, .spec editor - preferably with SLP extension, and a solidity editor - preferably with extension that has adequate support for reading and writing solidity code.
You may, however, choose to work with any other (textual) editor of your choice or split the work between several editors, just know that the SLP is currently only supported through VSCode.

</br>

- [x] Follow the [BankLesson1](BankLesson1) instructions to learn the basics of operating the Certora Prover.

</br>

- [x] Watch a lecture presented to the Opyn team by Dr. James Wilcox - [Link](https://youtu.be/YObi6qoyo_E). The lecture goes over the same examples from BankLesson1, explaining core concepts with more details.

</br>

---

## Running Scripts

</br>

Writing the `certoraRun` command in terminal every time we want to execute a run can be tiresome and uneasy on the eyes. Moreover, since a typical run of a single rule in real-life systems takes minutes to finish, we often work on 2 rules in parallel.

For that reason we often write a shell scripts of the run command that includes all the settings and options we need for a run. There are 4 advantages for using a script:

1. It is easier to read and sometimes can be more friendly to edit.
2. It can save a large chunk of code that's stored in a known place, as oppose to a terminal command that can be pushed down the stack and disappear after intense use of the terminal.
3. It can be uploaded to git or sent along with the specifications for others to use, instead of forcing them writing the command
4. It allows a more advance execution of run commands, e.g. running the exact same rule on every contract in a given directory (we will talk about sanity rule in the future).

</br>

- [ ] Follow the instructions on [RunScriptExample](RunScriptExample) to learn how to write run scripts, and how to execute the prover using scripts.

</br>

---

## Understanding Violations and Following Counter Examples

</br>

- [ ] Continue to next lesson: [Investigate Violations](../02.Lesson_InvestigateViolations) to exercise some more script writing and the art of understanding violations.

</br>

---
## Solutions to the lessons

</br>

- [ ] Some of the lessons in the Tutorials require you to write a `.spec` file containing your own rules for a given contract. Sometimes this can be quite challenging and if you get in trouble, you can have a look at the [Solutions](https://github.com/Certora/Tutorials/tree/master/Solutions) folder in the repository.

</br>

---

### Hurray! You've completed you first step towards being a security engineer

---
