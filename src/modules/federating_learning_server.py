# from src.modules.helper import read_addresses_and_keys_from_yaml, get_data
from src.modules.helper import Helper, get_data
from src.solidity_contract.contract import Contract
from src.solidity_contract.deploy import deploy_smart_contract
from src.solidity_contract.smart_contracts.job_finder import JobFinder
from src.solidity_contract.smart_contracts.fragmented_job_finder import (
    FragmentedJobFinder
)
from src.solidity_contract.smart_contracts.encryption_job_container import EncryptionJobContainer
from src.solidity_contract.smart_contracts.encryption_job_finder import (
    EncryptionJobFinder,
)


class FederatingLearningServer:
    def __init__(self, group_size, n_rounds, batch_size):
        address_and_private_key = Helper().read_addresses_and_keys_from_yaml(
            Helper(), for_worker=False
        )
        self.address = address_and_private_key[0]["address"]
        self.private_key = address_and_private_key[0]["private"]
        self.ip_address = "ip_addres_federating_learning_server"
        self.group_size = group_size  # n workers asked the same computation
        self.workers_addresses = []  # list of workers public addresses
        self.available_workers = (
            []
        )  # public address of workers ready to participate to the learning
        self.data = get_data()  # get data used for learning
        self.n_rounds = n_rounds  # number of rounds of the learning
        self.batch_size = batch_size  # number of data used for each round
        self.current_round = 0  # current round of the learning

    def deploy_contract(self, contract_file_name, contract_name):
        """Deploy a smart contract on the blockchain

        Args:
            contract_name (str): should end with "er" e.g not registering but register

        Returns:
            Contract: Contract instance
        """
        contract_adress, abi, bytecode = deploy_smart_contract(
            contract_file_name, contract_name, self.address, self.private_key
        )
        if contract_name == "JobFinder":
            return JobFinder(contract_name, contract_adress, abi, bytecode)
        elif contract_name == "FragmentedJobFinder":
            return FragmentedJobFinder(contract_name, contract_adress, abi, bytecode)
        elif contract_name == "EncryptionJobFinder":
            return EncryptionJobFinder(contract_name, contract_adress, abi, bytecode)
        elif contract_name == "EncryptionJobContainer":
            return EncryptionJobContainer(contract_name, contract_adress, abi, bytecode)
        else:
            return Contract(contract_name, contract_adress, abi, bytecode)

    def read_worker_addresses_from_smart_contract(self, contract):
        """Read workers addresses from smart contract

        Args:
            contract (Contract): Contract instance

        Returns:
            list: list of workers public addresses
        """
        workers_addresses = contract.get_workers()
        return workers_addresses

    def step(self, contract, network):
        """Handle every action server should perform:
        Check if new workers have registered to learning
        See if new results were sent by workers
        Decide if model can be updated based on current results and if yes, update it
        Ask workers to participate to next round of learning

        This method will be called inside the while loop of the main function as we run in sequential atm

        Args:
            contract (Contract): Contract instance
            network (Network): Network instance
        """

        # we start by checking if new workers have registered to the learning
        # if yes, we add them to the list of available workers
        workers_addresses = Helper().read_worker_addresses_from_smart_contract(contract)
        # add each address not in workers_addresses inside workers_addresses and available_workers
        for address in workers_addresses:
            if address not in self.workers_addresses:
                self.workers_addresses.append(address)
                self.available_workers.append(address)

        # check if we have new messages from workers
        new_messages = network.read_messages(self.ip_address)
        # each message is the result of a worker
        # TODO add proper handling of messages

        return
