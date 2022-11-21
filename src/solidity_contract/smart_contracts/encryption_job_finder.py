from web3 import Web3
from src.solidity_contract.contract import Contract


class EncryptionJobFinder(Contract):
    def __init__(self, contract_name, contract_address, abi, bytecode):
        super().__init__(contract_name, contract_address, abi, bytecode)
        self.web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))

    def get_job_container(self):
        return self.contract.functions.jobContainer().call()

    def get_job(self):
        """Should be call by a worker willing to participate to the learning

        Returns:
            (int, int): models weights, data indices to perform SGD
        """
        return self.contract.functions.getJob().call()

    def get_all_previous_jobs_best_model(self):
        return self.contract.functions.getAllPreviousJobsBestModel().call()

    def send_encrypted_model(
        self, encrypted_model_hex, worker_address, worker_private_key
    ):
        """Send the encrypted model to the blockchain
        Args:
            encrypted_model_hex (bytes[]): bytes array of the encrypted model
            worker_address (_type_): address of the worker
            worker_private_key (_type_): private key of the worker
        """
        # Sanize the worker address
        worker_address = Web3.toChecksumAddress(worker_address)
        register_tx = self.contract.functions.addEncryptedModel(
            worker_address, encrypted_model_hex
        ).build_transaction(
            {
                "gasPrice": 0,
                "from": worker_address,
                "nonce": self.web3.eth.get_transaction_count(worker_address),
            }
        )
        tx_receipt = super().sign_txs_and_send_it(worker_private_key, register_tx)
        return self.get_send_encrypted_model_return_value(self.web3, tx_receipt)

    def check_can_send_verification_parameters(self):
        """Check weather the worker can send the verification parameters

        Returns:
            boolean: true if the worker can send the verification parameters false otherwise
        """
        # TODO check
        return self.contract.functions.canSendVerificationParameters().call()

    def send_verifications_parameters(
        self, worker_nounce, worker_secret, worker_address, worker_private_key
    ):
        """Send the verification parameters to the blockchain (worker nounce, worker secret)

        Args:
            worker_nounce (int): _description_
            worker_secret (bytes[]): _description_
            worker_address (str): address of the worker
            worker_private_key (str): worker private key
        """
        # TODO check
        register_tx = self.contract.functions.addVerificationParameters(
            worker_address, worker_nounce, worker_secret
        ).build_transaction(
            {
                "gasPrice": 0,
                "from": Web3.toChecksumAddress(worker_address),
                "nonce": web3.eth.get_transaction_count(
                    Web3.toChecksumAddress(worker_address)
                ),
            }
        )
        tx_receipt = self.contract.sign_txs_and_send_it(
            worker_private_key, register_tx)
        return

    def parse_send_encrypted_model(self, result):
        return self.contract.web3.codec.decode_single(
            "bool", result
        )

    def get_send_encrypted_model_return_value(self, w3, txhash):
        try:
            tx = w3.eth.get_transaction(txhash)
        except Exception as e:
            print("Error getting transaction:", e)
            return None
        replay_tx = {
            'to': tx['to'],
            'from': tx['from'],
            'value': tx['value'],
            'data': tx['input'],
            'gas': tx['gas'],
        }
        # replay the transaction locally:
        try:
            ret = w3.eth.call(replay_tx, tx.blockNumber - 1)
            return (True, self.parse_send_encrypted_model(ret))
        except Exception as e:
            return (False, str(e))

    # -----------------Debug functions-----------------
    def get_received_models(self):
        return self.contract.functions.getReceivedModels().call()
