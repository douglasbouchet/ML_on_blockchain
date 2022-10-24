from web3 import Web3
from compile import abi

web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
print("web3 connected: {}".format(web3.isConnected()))

account_from = {
    "private_key": "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d",
    "address": "fce75e885241b4b465ad8e5919416ad4c9290d3e",
}

contract_address = (
    "0x641b0cf8B4685589C8DC18c79006585268783c15"  # depending on result of deploy.py
)
value = 3

print(
    f"Calling the increment by { value } function in contract at address: { contract_address }"
)

# 4. Create contract instance
Incrementer = web3.eth.contract(address=contract_address, abi=abi)

# 5. Build increment tx
increment_tx = Incrementer.functions.increment(value).buildTransaction(
    {
        "gasPrice": 0,
        "from": Web3.toChecksumAddress(account_from["address"]),
        "nonce": web3.eth.get_transaction_count(
            Web3.toChecksumAddress(account_from["address"])
        ),
    }
)

# 6. Sign tx with PK
tx_create = web3.eth.account.sign_transaction(increment_tx, account_from["private_key"])

# 7. Send tx and wait for receipt
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Tx successful with hash: { tx_receipt.transactionHash.hex() }")
