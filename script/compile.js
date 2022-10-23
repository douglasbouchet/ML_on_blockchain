const fs = require('fs').promises;
//const fs = import('fs.promises');
//import {default as fsWithCallbacks} from 'fs'
//const fs = fsWithCallbacks.promises
const solc = require('solc');
//const solc = import('solc');

async function main() {
  // Load the contract source code
  //const sourceCode = await fs.readFile('../smart-contract/SimpleStorage.sol', 'utf8');
  const sourceCode = await fs.readFile('/home/user/ml-blockchain/simple-transactions/smart-contract/SimpleStorage.sol', 'utf8');
  // Compile the source code and retrieve the ABI and bytecode
  const { abi, bytecode } = compile(sourceCode, 'SimpleStorage');
  // Store the ABI and bytecode into a JSON file
  const artifact = JSON.stringify({ abi, bytecode }, null, 2);
  await fs.writeFile('/home/user/ml-blockchain/simple-transactions/smart-contract/compiled-smart-contract/SimpleStorage.json', artifact);
}

function compile(sourceCode, contractName) {
  // Create the Solidity Compiler Standard Input and Output JSON
  const input = {
   language: 'Solidity',
   sources: { main: { content: sourceCode } },
   settings: { outputSelection: { '*': { '*': ['abi', 'evm.bytecode'] } } },
  };
  // Parse the compiler output to retrieve the ABI and bytecode
    const output = solc.compile(JSON.stringify(input));
    //console.log("output:" + output);
    const artifact = JSON.parse(output).contracts.main[contractName];
    //console.log("artifact:" + artifact);
  return {
    abi: artifact.abi,
    bytecode: artifact.evm.bytecode.object,
  };
}

main().then(() => process.exit(0));
