"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
exports.__esModule = true;
exports.invokeTransaction = exports.createTxBuilder = void 0;
var stellar_sdk_1 = require("stellar-sdk");
var server = new stellar_sdk_1.SorobanRpc.Server("https://soroban-testnet.stellar.org/");
// Contract information
var contractAddress = "CBJ5EI5S7GAKEDZYH4P7K477J7FRRD4F46BPCGQI5OU4SBI7G2CMZ7KH";
var contract = new stellar_sdk_1.Contract(contractAddress);
// Transaction submitter's keypair
var secretKey = ""; // Replace with actual secret key
var txSubmitterKeypair = stellar_sdk_1.Keypair.fromSecret(secretKey);
var to = "GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY"; //""
// Function name and arguments
var args = [
    new stellar_sdk_1.Address(to).toScVal(),
    (0, stellar_sdk_1.nativeToScVal)(666, { type: "i128" }),
];
function createTxBuilder(source) {
    return __awaiter(this, void 0, void 0, function () {
        var sourceAccount, e_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, server.getAccount(source.publicKey())];
                case 1:
                    sourceAccount = _a.sent();
                    return [2 /*return*/, new stellar_sdk_1.TransactionBuilder(sourceAccount, {
                            fee: "10000",
                            timebounds: { minTime: 0, maxTime: 0 },
                            networkPassphrase: "Test SDF Network ; September 2015"
                        })];
                case 2:
                    e_1 = _a.sent();
                    console.error(e_1);
                    throw Error("unable to create txBuilder");
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.createTxBuilder = createTxBuilder;
function invokeTransaction(prepped_tx, source, sim) {
    return __awaiter(this, void 0, void 0, function () {
        var tx_hash, response, status;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    tx_hash = prepped_tx.hash().toString("hex");
                    console.log("submitting tx...");
                    return [4 /*yield*/, server.sendTransaction(prepped_tx)];
                case 1:
                    response = _a.sent();
                    status = response.status;
                    _a.label = 2;
                case 2:
                    if (!(status === "PENDING" || status === "NOT_FOUND")) return [3 /*break*/, 5];
                    // See if the transaction is complete
                    return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve, 2000); })];
                case 3:
                    // See if the transaction is complete
                    _a.sent();
                    console.log("checking tx...");
                    return [4 /*yield*/, server.getTransaction(tx_hash)];
                case 4:
                    response = _a.sent();
                    status = response.status;
                    console.log(response);
                    return [3 /*break*/, 2];
                case 5: return [2 /*return*/, response];
            }
        });
    });
}
exports.invokeTransaction = invokeTransaction;
function main() {
    return __awaiter(this, void 0, void 0, function () {
        var txBuilder, operation, tx, preparedTransaction, response, e_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 4, , 5]);
                    console.log(txSubmitterKeypair.publicKey());
                    return [4 /*yield*/, createTxBuilder(txSubmitterKeypair)];
                case 1:
                    txBuilder = _a.sent();
                    operation = contract.call.apply(contract, __spreadArray(["mint"], args, false));
                    if (typeof operation === "string") {
                        operation = stellar_sdk_1.xdr.Operation.fromXDR(operation, "base64");
                    }
                    txBuilder.addOperation(operation);
                    tx = txBuilder.build();
                    return [4 /*yield*/, server.prepareTransaction(tx)];
                case 2:
                    preparedTransaction = _a.sent();
                    preparedTransaction.sign(txSubmitterKeypair);
                    return [4 /*yield*/, invokeTransaction(preparedTransaction, txSubmitterKeypair, false)];
                case 3:
                    response = _a.sent();
                    return [3 /*break*/, 5];
                case 4:
                    e_2 = _a.sent();
                    console.error("Error occurred:", e_2);
                    return [3 /*break*/, 5];
                case 5: return [2 /*return*/];
            }
        });
    });
}
main();
