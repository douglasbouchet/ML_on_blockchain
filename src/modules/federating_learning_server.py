# from src.modules.helper import read_addresses_and_keys_from_yaml, get_data
from src.modules.helper import *
from src.solidity_contract.deploy import deploy_smart_contract


class FederatingLearningServer:
    def __init__(self, group_size, n_rounds, batch_size):
        address_and_private_key = Helper().read_addresses_and_keys_from_yaml(
            Helper(), for_worker=False
        )
        self.address = address_and_private_key[0]["address"]
        self.private_key = address_and_private_key[0]["private"]
        self.ip_address = "ip_addres_federating_learning_server"
        self.group_size = group_size  # n workers asked the same computation
        self.available_workers = (
            []
        )  # public address of workers ready to participate to the learning
        self.data = get_data()  # get data used for learning
        self.n_rounds = n_rounds  # number of rounds of the learning
        self.batch_size = batch_size  # number of data used for each round
        self.current_round = 0  # current round of the learning

    def deploy_contract(self, contract_name):
        """Deploy a smart contract on the blockchain

        Args:
            contract_name (str): should end with "er" e.g not registering but register

        Returns:
            Contract: Contract instance
        """
        contract_adress, abi, bytecode = deploy_smart_contract(
            contract_name, self.from_address, self.from_private_key
        )
        contract = Contract(contract_name, contract_adress, abi, bytecode)
        return contract

    def step():
        """Handle every action server should perform:
        Check if new workers have registered to learning
        See if new results were sent by workers
        Decide if model can be updated based on current results and if yes, update it
        Ask workers to participate to next round of learning

        This method will be called inside the while loop of the main function as we run in sequential atm
        """

        # TODO

        return
