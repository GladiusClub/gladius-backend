const StellarSdk = require("@stellar/stellar-sdk");
const {
  SorobanRpc,
  xdr,
  Keypair,
  Networks,
  TransactionBuilder,
  Operation,
  nativeToScVal,
  Address,
  Contract,
  BASE_FEE,
} = StellarSdk;

const server = new SorobanRpc.Server("https://soroban-testnet.stellar.org:443");

// Contract information
const contractAddress =
  "CBJ5EI5S7GAKEDZYH4P7K477J7FRRD4F46BPCGQI5OU4SBI7G2CMZ7KH";
const contract = new Contract(contractAddress);

// Transaction submitter's keypair
const secretKey = ""; // Replace with actual secret key
const txSubmitterKeypair = Keypair.fromSecret(secretKey);

console.log("Public Key:", txSubmitterKeypair.publicKey());

// Function name and arguments
const args = [
  new Address(txSubmitterKeypair.publicKey()).toScVal(),
  nativeToScVal(1000, { type: "i128" }),
];
(async () => {
  // Load the account of the transaction submitter
  const sourceAccount = await server.getAccount(txSubmitterKeypair.publicKey());

  // Build the transaction
  const builtTransaction = new TransactionBuilder(sourceAccount, {
    fee: BASE_FEE,
    networkPassphrase: Networks.TESTNET,
  })
    .addOperation(contract.call("mint", ...args))
    .setTimeout(30)
    .build();

  let preparedTransaction = await server.prepareTransaction(builtTransaction);

  // Sign the transaction with the source account's keypair.
  preparedTransaction.sign(txSubmitterKeypair);

  console.log(
    `Signed prepared transaction XDR: ${preparedTransaction
      .toEnvelope()
      .toXDR("base64")}`
  );

  try {
    let sendResponse = await server.sendTransaction(preparedTransaction);
    console.log(`Sent transaction: ${JSON.stringify(sendResponse)}`);

    if (sendResponse.status === "PENDING") {
      let getResponse = await server.getTransaction(sendResponse.hash);
      // Poll `getTransaction` until the status is not "NOT_FOUND"
      while (getResponse.status === "NOT_FOUND") {
        console.log("Waiting for transaction confirmation...");
        // See if the transaction is complete
        getResponse = await server.getTransaction(sendResponse.hash);
        // Wait one second
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }

      //console.log(`getTransaction response: ${JSON.stringify(getResponse)}`);

      if (getResponse.status === "SUCCESS") {
        // Make sure the transaction's resultMetaXDR is not empty
        if (!getResponse.resultMetaXdr) {
          throw "Empty resultMetaXDR in getTransaction response";
        }
        // Find the return value from the contract and return it
        let transactionMeta = getResponse.resultMetaXdr;
        let returnValue = getResponse.returnValue;
        console.log(`Transaction result: ${returnValue.value()}`);
      } else {
        console.log(
          "ERROR: ",
          JSON.stringify(
            StellarSdk.xdr.TransactionEnvelope.fromXDR(
              getResponse.envelope_xdr,
              "base64"
            )
          )
        );
        throw `Transaction failed: ${getResponse.resultXdr}`;
      }
    } else {
      throw sendResponse.errorResultXdr;
    }
  } catch (err) {
    // Catch and report any errors we've thrown
    console.log("Sending transaction failed");
    console.log(JSON.stringify(err));
  }
})();
