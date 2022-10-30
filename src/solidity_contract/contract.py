from web3 import Web3


class Contract:
    def __init__(self, contract_name, contract_address, abi, bytecode):
        self.contract_name = contract_name
        self.contract_address = contract_address
        self.abi = abi
        self.bytecode = bytecode
        self.web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
        self.contract = self.web3.eth.contract(
            address=self.contract_address, abi=self.abi
        )

    # def get_number_of_workers(self):
    #     return self.contract.functions.number().call()

    def get_number_of_workers(self):
        return len(self.contract.functions.getWorkers().call())

    def get_workers(self):
        workers_addresses = self.contract.functions.getWorkers().call()
        # for each address, remove the 0x and lower case it
        return [worker_address[2:].lower() for worker_address in workers_addresses]
