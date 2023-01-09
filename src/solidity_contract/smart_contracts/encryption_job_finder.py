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

    def compare_hash(self, model_hash, worker_address, worker_private_key):
        worker_address = Web3.toChecksumAddress(worker_address)
        try:
            register_tx = self.contract.functions.compareKeccak(
                model_hash
            ).build_transaction(
                {
                    "gasPrice": 0,
                    "from": worker_address,
                    "nonce": self.web3.eth.get_transaction_count(worker_address),
                }
            )
            tx_receipt = super().sign_txs_and_send_it(worker_private_key, register_tx)
            return self.get_compare_hash(self.web3, tx_receipt)
        except Exception as e:
            print("Error compare_hash:", e)
            return False

    # def send_encrypted_model(
    def send_hashed_model(
        self, encrypted_model_hash, worker_address, worker_private_key
    ):
        """Send the encrypted model to the blockchain
        Args:
            encrypted_model_hash (bytes[]): bytes array of hash of the model xored with the worker secret
            worker_address (str): address of the worker
            worker_private_key (str): private key of the worker
        """
        # Sanize the worker address
        worker_address = Web3.toChecksumAddress(worker_address)
        try:
            register_tx = self.contract.functions.addEncryptedModel(
                int(worker_address, 16), encrypted_model_hash
            ).build_transaction(
                {
                    "gasPrice": 0,
                    "from": worker_address,
                    "nonce": self.web3.eth.get_transaction_count(worker_address),
                }
            )
            tx_receipt = super().sign_txs_and_send_it(worker_private_key, register_tx)
            return self.get_send_encrypted_model_return_value(self.web3, tx_receipt)
        except Exception as e:
            print("Error sending encrypted model:", e)
            return [False]

    def check_can_send_verification_parameters(self, worker_address):
        """Check weather the worker can send the verification parameters
        True if worker did send a model and if job has received enough models

        Args:
            worker_address (address): address of the worker
        Returns:
            boolean: true if the worker can send the verification parameters false otherwise
        """
        # TODO check
        return self.contract.functions.canSendVerificationParameters(Web3.toChecksumAddress(worker_address)).call()

    def send_verifications_parameters(
        self,
        clear_model,
        worker_address,
        worker_private_key,
    ) -> bool:
        """Send the verification parameters to the blockchain (worker nounce, worker secret)

        Args:
            clear_model (int): the model as an integer (simple atm)
            worker_address (str): address of the worker
            worker_private_key (str): private key of the worker
        return: true if the transaction is successful false otherwise
        """
        worker_address = Web3.toChecksumAddress(worker_address)
        # add the worker address to the clear model inside a new array (as expected by the smart contract)
        array = [int(worker_address, 16)] + clear_model
        try:
            register_tx = self.contract.functions.addVerificationParameters(
                array
            ).build_transaction(
                {
                    "gasPrice": 0,
                    "from": worker_address,
                    "nonce": self.web3.eth.get_transaction_count(worker_address),
                }
            )
            _ = super().sign_txs_and_send_it(worker_private_key, register_tx)
        except Exception as e:
            print("Error sending verification parameters:", e)
            return False
        return True

    def parse_send_encrypted_model(self, result):
        return self.contract.web3.codec.decode_single("bool", result)

    def get_send_encrypted_model_return_value(self, w3, txhash):
        try:
            tx = w3.eth.get_transaction(txhash)
        except Exception as e:
            print("Error getting transaction:", e)
            return None
        replay_tx = {
            "to": tx["to"],
            "from": tx["from"],
            "value": tx["value"],
            "data": tx["input"],
            "gas": tx["gas"],
        }
        # replay the transaction locally:
        try:
            ret = w3.eth.call(replay_tx, tx.blockNumber - 1)
            return (True, self.parse_send_encrypted_model(ret))
        except Exception as e:
            return (False, str(e))

    def get_compare_hash(self, w3, txhash):
        try:
            tx = w3.eth.get_transaction(txhash)
        except Exception as e:
            print("Error getting transaction:", e)
            return None
        replay_tx = {
            "to": tx["to"],
            "from": tx["from"],
            "value": tx["value"],
            "data": tx["input"],
            "gas": tx["gas"],
        }
        # replay the transaction locally:
        try:
            ret = w3.eth.call(replay_tx, tx.blockNumber - 1)
            return self.parse_send_encrypted_model(ret)
        except Exception as e:
            print("Error replaying transaction:", e)
            return False

    def get_final_model(self):
        return self.contract.functions.getFinalModel().call()

    # -----------------Debug functions-----------------
    def get_received_models(self):
        return self.contract.functions.getReceivedModels().call()

    def get_model_is_ready(self):
        return self.contract.functions.getModelIsready().call()

    def get_keccak(self, clear_model):
        clear_model = [clear_model[i: i + 1]
                       for i in range(0, len(clear_model), 1)]
        ret = self.contract.functions.computeKeccak256(clear_model).call()
        # parse the ret to get the hash
        return self.contract.web3.codec.decode_single("bytes32", ret)
        # return self.contract.functions.computeKeccak256(clear_model).call()
        # return self.contract.functions.computeKeccak256().call()
