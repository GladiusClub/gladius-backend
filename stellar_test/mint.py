"""This example demonstrates how to invoke an auth contract with [Transaction Invoker] authrization.

See https://soroban.stellar.org/docs/how-to-guides/auth
See https://soroban.stellar.org/docs/learn/authorization#transaction-invoker
"""
import time

from stellar_sdk import Keypair, Network, SorobanServer, TransactionBuilder, scval
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.exceptions import PrepareTransactionException
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

rpc_server_url = "https://soroban-testnet.stellar.org:443"
soroban_server = SorobanServer(rpc_server_url)
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

contract_id = "CBJ5EI5S7GAKEDZYH4P7K477J7FRRD4F46BPCGQI5OU4SBI7G2CMZ7KH"
tx_submitter_kp = Keypair.from_secret(
    ""
)

print("public key; ", tx_submitter_kp.public_key)

# to_address
to_address ='GALT6V5AXC56AS6XY6XIKET25I3GRII2EIMSXFBVKGGSQT3AKQNLCETY'

func_name = "mint"
args = [
    scval.to_address(to_address),
    scval.to_int128(444)
]



source = soroban_server.load_account(tx_submitter_kp.public_key)
tx = (
    TransactionBuilder(source, network_passphrase, base_fee=100)
    .add_time_bounds(0, 0)
    .append_invoke_contract_function_op(
        contract_id=contract_id,
        function_name=func_name,
        parameters=args,
    )
    .build()
)

try:
    tx = soroban_server.prepare_transaction(tx)
except PrepareTransactionException as e:
    print(f"Got exception: {e.simulate_transaction_response}")
    raise e

tx.sign(tx_submitter_kp)
print(f"Signed XDR:\n{tx.to_xdr()}")

send_transaction_data = soroban_server.send_transaction(tx)
print(f"sent transaction: {send_transaction_data}")
if send_transaction_data.status != SendTransactionStatus.PENDING:
    raise Exception("send transaction failed")

while True:
    print("waiting for transaction to be confirmed...")
    get_transaction_data = soroban_server.get_transaction(send_transaction_data.hash)
    if get_transaction_data.status != GetTransactionStatus.NOT_FOUND:
        break
    time.sleep(3)

print(f"transaction: {get_transaction_data}")

if get_transaction_data.status == GetTransactionStatus.SUCCESS:
    assert get_transaction_data.result_meta_xdr is not None
    transaction_meta = stellar_xdr.TransactionMeta.from_xdr(
        get_transaction_data.result_meta_xdr
    )
    result = transaction_meta.v3.soroban_meta.return_value.u32  # type: ignore
    print(f"Function result: {result}")
else:
    print(f"Transaction failed: {get_transaction_data.result_xdr}")