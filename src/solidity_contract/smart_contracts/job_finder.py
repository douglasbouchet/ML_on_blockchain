from web3 import Web3
from src.solidity_contract.contract import Contract


class JobFinder(Contract):
    def __init__(self, contract_name, contract_address, abi, bytecode):
        super().__init__(contract_name, contract_address, abi, bytecode)

    def get_job_container(self):
        return self.contract.functions.jobContainer().call()

    def get_n_models_until_end(self):
        return self.contract.functions.getNModelsUntilEnd().call()

    def get_job(self):
        """Should be call by a worker willing to participate to the learning

        Returns:
            (int[], int[]): models weights, data indices to perform SGD
        """

        return self.contract.functions.getJob().call()

    def submit_new_model(self, new_model, worker_address, worker_private_key):
        """This function is called whenever a worker wants to submit a new model to the job.
        If the job complete after receiving this worker, the job's resulting model is published on the blockchain and
        a new job is created.

        TODO add check such that worker submitted for a previous job don't actually put wieghts for the current job
        Args:
            new_model (int): new computed weights of the model by the worker
            worker_address (str): worker public address
        """
        web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))

        # 4. Create contract instance
        # contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        # 5. Build increment tx
        # register_tx = contract.functions.register_worker().buildTransaction(
        register_tx = self.contract.functions.submitNewModel(
            new_model
        ).buildTransaction(
            {
                "gasPrice": 0,
                "from": Web3.toChecksumAddress(worker_address),
                "nonce": web3.eth.get_transaction_count(
                    Web3.toChecksumAddress(worker_address)
                ),
            }
        )

        # 6. Sign tx with PK
        tx_create = web3.eth.account.sign_transaction(register_tx, worker_private_key)

        # 7. Send tx and wait for receipt
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    # -----------------Debug functions-----------------
    def get_received_models(self):
        return self.contract.functions.getReceivedModels().call()
