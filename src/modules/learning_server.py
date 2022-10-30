from src.solidity_contract.contract import Contract
from src.solidity_contract.deploy import deploy_smart_contract


class LearningServer:
    def __init__(self, from_address, from_private_key):
        self.from_address = from_address
        self.from_private_key = from_private_key
        self.ip_address = "ip_addres_learning_server"

    def deploy(self, contract_name):
        """_summary_

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
