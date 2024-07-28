import {
  SorobanRpc,
  Address,
  Contract,
  Keypair,
  Networks,
  nativeToScVal,
  xdr,
  TransactionBuilder,
  Transaction,
} from  "@stellar/stellar-sdk";

type txResponse =
  | SorobanRpc.Api.SendTransactionResponse
  | SorobanRpc.Api.GetTransactionResponse;
type txStatus =
  | SorobanRpc.Api.SendTransactionStatus
  | SorobanRpc.Api.GetTransactionStatus;

const server = new SorobanRpc.Server("https://soroban-testnet.stellar.org/");

// Contract information
const contractAddress =
  "CBJ5EI5S7GAKEDZYH4P7K477J7FRRD4F46BPCGQI5OU4SBI7G2CMZ7KH";
const contract = new Contract(contractAddress);

// Transaction submitter's keypair
const secretKey = ""; // Replace with actual secret key
const txSubmitterKeypair = Keypair.fromSecret(secretKey);
const to = "GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY"; //""
// Function name and arguments
const args: xdr.ScVal[] = [
  new Address(to).toScVal(),
  nativeToScVal(666, { type: "i128" }),
];

export async function createTxBuilder(
  source: Keypair
): Promise<TransactionBuilder> {
  try {
    const sourceAccount = await server.getAccount(source.publicKey());
    return new TransactionBuilder(sourceAccount, {
      fee: "10000", // Hardcoded fee
      timebounds: { minTime: 0, maxTime: 0 },
      networkPassphrase: "Test SDF Network ; September 2015", // Hardcoded passphrase
    });
  } catch (e: any) {
    console.error(e);
    throw Error("unable to create txBuilder");
  }
}

export async function invokeTransaction(
  prepped_tx: Transaction,
  source: Keypair,
  sim: boolean
) {
  const tx_hash = prepped_tx.hash().toString("hex");
  console.log("submitting tx...");
  let response: txResponse = await server.sendTransaction(prepped_tx);
  let status: txStatus = response.status;
  // Poll this until the status is not "NOT_FOUND"
  while (status === "PENDING" || status === "NOT_FOUND") {
    // See if the transaction is complete
    await new Promise((resolve) => setTimeout(resolve, 2000));
    console.log("checking tx...");
    response = await server.getTransaction(tx_hash);
    status = response.status;
    console.log(response);
  }
  return response;
}

async function main() {
  try {
    console.log(txSubmitterKeypair.publicKey());
    const txBuilder = await createTxBuilder(txSubmitterKeypair);
    let operation = contract.call("mint", ...args);
    if (typeof operation === "string") {
      operation = xdr.Operation.fromXDR(operation, "base64");
    }
    txBuilder.addOperation(operation);
    const tx = txBuilder.build();

    let preparedTransaction = await server.prepareTransaction(tx);
    preparedTransaction.sign(txSubmitterKeypair);

    let response = await invokeTransaction(
      preparedTransaction,
      txSubmitterKeypair,
      false
    );

    // Additional transaction building steps go here
  } catch (e) {
    console.error("Error occurred:", e);
  }
}

main();
