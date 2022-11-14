from web3 import Web3
from src.solidity_contract.contract import Contract


class FragmentedJobFinder(Contract):
    def __init__(self, contract_name, contract_address, abi, bytecode):
        super().__init__(contract_name, contract_address, abi, bytecode)

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

    def parse_add_fragment_result(self, result):
        return self.contract.web3.codec.decode_single(
            "bool", result
        )

    def get_TX_result(self, w3, txhash):
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
            # return (True, ret)
            return (True, self.parse_add_fragment_result(ret))
        except Exception as e:
            return (False, str(e))

    def add_fragment(self, _fragNb, _weight, _modelHash, worker_address, worker_private_key):
        """This function is called whenever a worker wants to submit a new fragment to the job.
        If the job complete after receiving this worker, the job's resulting model is published on the blockchain and
        a new job is created.

        TODO add check such that worker submitted for a previous job don't actually put wieghts for the current job
        Args:
            _fragNb (int): the number of the fragment
            _weight (int): the weight of the fragment
            _modelHash (str): the hash of the complete model
            worker_address (str): worker public address
            worker_private_key (str): worker private key, used to sign the transaction
        """
        #web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
        web3 = self.contract.web3
        register_tx = self.contract.functions.addFragment(
            _fragNb, _weight, _modelHash
        ).build_transaction(
            {
                "gasPrice": 0,
                "from": Web3.toChecksumAddress(worker_address),
                "nonce": web3.eth.get_transaction_count(
                    Web3.toChecksumAddress(worker_address)
                ),
            }
        )

        # 6. Sign tx with PK
        tx_create = web3.eth.account.sign_transaction(
            register_tx, worker_private_key)
        # 7. Send tx and wait for receipt
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return self.get_TX_result(web3, tx_hash)

    # -----------------Debug functions-----------------
    def get_received_models(self):
        return self.contract.functions.getReceivedModels().call()
