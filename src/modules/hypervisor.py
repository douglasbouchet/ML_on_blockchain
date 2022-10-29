from src.modules.worker import Worker
from src.modules.helper import Helper
from src.modules.contract import Contract


class Hypervisor:
    """Manage the workers in order to perform distributed learning
    Contains method to add new workers, make them participate into learning or stop participating
    to the learning

    workers: list of workers
    address_to_key: dict of public address to private key
    """

    def __init__(self):
        self.workers = []
        self.address_to_key = Helper.read_addresses_and_keys_from_yaml(
            Helper, for_worker=True
        )
        self.contract = None
        self.ip_address = "hypervisor_ip_address"

    def create_worker(self):
        """Add a worker to the list of workers (maximum 999 workers as no more addresses)

        Returns: the worker if added, None otherwise
        """
        # check if we don't have created more workers than the number of addresses
        if len(self.workers) < len(self.address_to_key):
            address_and_key = self.address_to_key[len(self.workers)]
            print(address_and_key)
            worker = Worker(address_and_key["address"], address_and_key["private"])
            self.workers.append(worker)
            return worker
        else:
            return None

    def remove_worker(self, worker_public_address):
        """Remove a worker from the list of workers

        Args:
            worker_public_address (string): the public address of the worker to remove

        Returns: the worker if removed, None otherwise
        """
        for worker in self.workers:
            if worker.address == worker_public_address:
                self.workers.remove(worker)
                return worker
        return None

    def make_worker_join_learning(self, worker):
        """Make a worker participate to the learning

        Args:
            worker (Worker): the worker to make participate to the learning
        """
        # if contract abi and addresses aren't available do nothing
        if self.contract is None:
            print("No contract found, please deploy a contract first")
            return
        if worker not in self.workers:
            print("This worker is not managed by this hypervisor")
            return
        worker.register_to_learning(self.contract.contract_address, self.contract.abi)

    def make_worker_leave_learning(self, worker):
        """Make a worker stop participating to the learning

        Args:
            worker (Worker): the worker to make stop participating to the learning
        """
        if self.contract is None:
            print("No contract found, please deploy a contract first")
            return
        if worker not in self.workers:
            print("This worker is not managed by this hypervisor")
            return
        worker.unregister_from_learning(
            self.contract.contract_address, self.contract.abi
        )

    def set_contract(self, contract):
        """Set the contract to use for the learning

        Args:
            contract (Contract): the contract to use for the learning
        """
        assert type(contract) == Contract
        self.contract = contract
