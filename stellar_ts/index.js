import * as functions from 'firebase-functions';
import { SorobanRpc, Address, Contract, Keypair, nativeToScVal, xdr, TransactionBuilder, } from "stellar-sdk";
const server = new SorobanRpc.Server("https://soroban-testnet.stellar.org/");
const contractAddress = "CBJ5EI5S7GAKEDZYH4P7K477J7FRRD4F46BPCGQI5OU4SBI7G2CMZ7KH";
const contract = new Contract(contractAddress);
async function createTxBuilder(source) {
    try {
        const sourceAccount = await server.getAccount(source.publicKey());
        return new TransactionBuilder(sourceAccount, {
            fee: "10000", // Hardcoded fee
            timebounds: { minTime: 0, maxTime: 0 },
            networkPassphrase: "Test SDF Network ; September 2015", // Adjusted for clarity
        });
    }
    catch (e) {
        console.error(e);
        throw new Error("unable to create txBuilder");
    }
}
async function invokeTransaction(prepped_tx, source, sim) {
    const tx_hash = prepped_tx.hash().toString("hex");
    console.log("submitting tx...");
    let response = await server.sendTransaction(prepped_tx);
    let status = response.status; // Type casting for simplicity
    while (status === "PENDING" || status === "NOT_FOUND") {
        await new Promise((resolve) => setTimeout(resolve, 2000));
        console.log("checking tx...");
        response = await server.getTransaction(tx_hash);
        status = response.status; // Adjust based on actual API response
        console.log(response);
    }
    return response;
}
export const StellarGladiusContracts = functions.https.onRequest(async (req, res) => {
    const secretKey = "SBJTRWSLGANJMFKZG4PUZMDHFLJHFOZC6OFB3XS25UDMQD337NQZDLAN"; // Ensure to securely manage this secret
    const txSubmitterKeypair = Keypair.fromSecret(secretKey);
    const { contract_func, to_address, amount } = req.body;
    // example parameters
    // const contract_func = "mint",
    // const to = "GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY";
    // const amount = 111
    const args = [
        new Address(to_address).toScVal(),
        nativeToScVal(amount, { type: "i128" }),
    ];
    try {
        console.log(txSubmitterKeypair.publicKey());
        const txBuilder = await createTxBuilder(txSubmitterKeypair);
        let operation = contract.call(contract_func, ...args);
        if (typeof operation === "string") {
            operation = xdr.Operation.fromXDR(operation, "base64");
        }
        txBuilder.addOperation(operation);
        const tx = txBuilder.build();
        let preparedTransaction = await server.prepareTransaction(tx);
        preparedTransaction.sign(txSubmitterKeypair);
        let response = await invokeTransaction(preparedTransaction, txSubmitterKeypair, false);
        res.status(200).send("Operation Successful");
    }
    catch (error) {
        console.error("Error occurred:", error);
        res.status(500).send("Operation Failed");
    }
});
