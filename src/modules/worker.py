from web3 import Web3


class Worker:
    def __init__(self, address, private_key):
        self.address = address
        self.private_key = private_key

    def register_to_learning(self, contract_address, contract_abi):

        web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
        account_from = {
            "private_key": "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d",
            "address": "fce75e885241b4b465ad8e5919416ad4c9290d3e",
        }
        value = 1

        print(
            f"Calling the increment by { value } function in contract at address: { contract_address }"
        )

        # 4. Create contract instance
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # 5. Build increment tx
        # increment_tx = contract.functions.increment(value).buildTransaction(
        register_tx = contract.functions.register_worker().buildTransaction(
            {
                "gasPrice": 0,
                "from": Web3.toChecksumAddress(self.address),
                "nonce": web3.eth.get_transaction_count(
                    Web3.toChecksumAddress(self.address)
                ),
            }
        )

        # 6. Sign tx with PK
        tx_create = web3.eth.account.sign_transaction(register_tx, self.private_key)

        # 7. Send tx and wait for receipt
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print(
            f"Tx successful with hash: { tx_receipt.transactionHash.hex() } for incrementing the number"
        )
