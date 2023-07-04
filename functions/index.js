// env variables in use
// $WEB3_INFURA_PROJECT_ID'
// $LATEST_CONTRACT_ADDRESS;
// $CONTRACT_OWNER_PRIVATE_KEY
// $CONTRACT_OWNER_ADDRESS

const Web3 = require('web3');
const web3 = new Web3('https://polygon-mumbai.infura.io/v3/$WEB3_INFURA_PROJECT_ID');

const contractAddress = $LATEST_CONTRACT_ADDRESS; // Replace with your contract address
const privateKey = $CONTRACT_OWNER_PRIVATE_KEY; // Replace with your private key

const contractJson = require('../polygon_test/build/contracts/GLCToken.json');

const contract = new web3.eth.Contract(contractJson.abi, contractAddress);

async function mintTokens(userAddress, amount) {
  const nonce = await web3.eth.getTransactionCount($CONTRACT_OWNER_ADDRESS); // replace  with the sender's address
  const gasPrice = await web3.eth.getGasPrice();
  const gasLimit = 100000;

  const data = contract.methods.mint(userAddress, amount).encodeABI();

  const tx = {
    nonce: nonce,
    gasPrice: gasPrice,
    gasLimit: gasLimit,
    to: contractAddress,
    value: 0,
    data: data
  };

  const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);

  const receipt = await web3.eth.sendSignedTransaction(signedTx.rawTransaction);

  console.log(`Transaction hash: ${receipt.transactionHash}`);
}