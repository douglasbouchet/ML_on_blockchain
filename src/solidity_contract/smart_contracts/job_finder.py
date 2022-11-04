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
