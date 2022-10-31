import src.communication.network
from src.modules.worker import Worker
from src.modules.mnist_worker import MnsitWorker
from src.modules.helper import Helper
from src.solidity_contract.contract import Contract


class Hypervisor:
    """Manage the workers in order to perform distributed learning
    Contains method to add new workers, make them participate into learning or stop participating
    to the learning

    workers: list of workers
    address_to_key: dict of public address to private key
    """

    def __init__(self):
        self.address_to_workers = {}  # dict of address to worker
        self.address_to_key = Helper.read_addresses_and_keys_from_yaml(
            Helper, for_worker=True
        )
        self.address_used = []  # usefull as we don't want to use the same address twice
        self.contract = None
        self.ip_address = "hypervisor_ip_address"

    def create_worker(self):
        """Add a worker to the list of workers (maximum 999 workers as no more addresses)

        Returns: the worker if added, None otherwise
        """
        # check if we don't have created more workers than the number of addresses
        if len(self.address_used) < len(self.address_to_key):
            address_and_key = self.address_to_key[len(self.address_used)]
            self.address_used.append(address_and_key["address"])
            worker = Worker(address_and_key["address"], address_and_key["private"])
            self.address_to_workers[worker.address] = worker
            return worker
        else:
            return None

    def create_mnist_worker(self):
        """Add a worker to the list of workers (maximum 999 workers as no more addresses)

        Returns: the worker if added, None otherwise
        """
        # check if we don't have created more workers than the number of addresses
        if len(self.address_used) < len(self.address_to_key):
            address_and_key = self.address_to_key[len(self.address_used)]
            self.address_used.append(address_and_key["address"])
            mnist_worker = MnsitWorker(
                address_and_key["address"], address_and_key["private"]
            )
            self.address_to_workers[mnist_worker.address] = mnist_worker
            return mnist_worker
        else:
            return None

    def remove_worker(self, worker_public_address):
        """Remove a worker from the list of workers

        Args:
            worker_public_address (string): the public address of the worker to remove

        Returns: the worker if removed, None otherwise
        """
        if worker_public_address in self.address_to_workers:
            worker = self.address_to_workers[worker_public_address]
            del self.address_to_workers[worker_public_address]
            return worker
        else:
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
        if worker.address not in self.address_to_workers:
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
        if worker.address not in self.address_to_workers:
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

    def handle_messages(self, network):
        """Handle the messages received from the workers

        Args:
            network (Network): Network instance, used to read the messages
        """

        # get the list of new messages
        messages = network.read_messages(self.ip_address)
        print("Hypervisor received {} messages".format(len(messages)))

        # messages are only from learning server atm.
        for message in messages:
            worker_address = message.get_worker_address()
            model_weight = message.get_model_weight()
            # check if the worker is managed by this hypervisor
            if worker_address in self.address_to_workers:
                # update the model of the worker
                self.address_to_workers[worker_address].get_new_model_weigths(
                    model_weight
                )
            else:
                print(
                    "[handle_messages]: This worker is not managed by this hypervisor"
                )
