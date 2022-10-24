# 1. Import the ABI and bytecode
from web3 import Web3

# from compile import abi, bytecode
from .compile import compile_smart_contract

# # 2. Add the Web3 provider logic here:
# web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
# print("web3 connected: {}".format(web3.isConnected()))

# # 3. Create address variable
# account_from = {
#     "private_key": "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d",
#     "address": "fce75e885241b4b465ad8e5919416ad4c9290d3e",
# }

# print(f'Attempting to deploy from account: { account_from["address"] }')

# # 4. Create contract instance
# Incrementer = web3.eth.contract(abi=abi, bytecode=bytecode)

# # 5. Build constructor tx
# construct_txn = Incrementer.constructor(5).buildTransaction(
#     {
#         "gasPrice": 0,
#         "from": Web3.toChecksumAddress(account_from["address"]),
#         "nonce": web3.eth.get_transaction_count(
#             Web3.toChecksumAddress(account_from["address"])
#         ),
#     }
# )

# # 6. Sign tx with PK
# tx_create = web3.eth.account.sign_transaction(
#     construct_txn, account_from["private_key"]
# )

# # 7. Send tx and wait for receipt
# tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# print(f"Contract deployed at address: { tx_receipt.contractAddress }")


def deploy_smart_contract(contract_name, from_address, from_private_key):
    # 2. Add the Web3 provider logic here:
    web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
    print("web3 connected: {}".format(web3.isConnected()))

    # 3. Create address variable
    account_from = {
        "private_key": from_private_key,
        "address": from_address,
    }

    print(f'Attempting to deploy from account: { account_from["address"] }')

    # get abi and bytecode from compiled contract
    abi, bytecode = compile_smart_contract(contract_name)

    new_contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    # 5. Build constructor tx
    # construct_txn = new_contract.constructor(5).buildTransaction(
    construct_txn = new_contract.constructor(
        0
    ).buildTransaction(  # TODO modify here the syntax of constructor depending on the smart contract
        {
            "gasPrice": 0,
            "from": Web3.toChecksumAddress(account_from["address"]),
            "nonce": web3.eth.get_transaction_count(
                Web3.toChecksumAddress(account_from["address"])
            ),
        }
    )

    # 6. Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(
        construct_txn, account_from["private_key"]
    )

    # 7. Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract deployed at address: { tx_receipt.contractAddress }")
    return tx_receipt.contractAddress, abi, bytecode
