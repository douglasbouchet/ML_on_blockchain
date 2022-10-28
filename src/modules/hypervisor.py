from src.modules.worker import Worker
from src.modules.helper import Helper


class Hypervisor:
    """Manage the workers in order to perform distributed learning
    Contains method to add new workers, make them participate into learning or stop participating
    to the learning

    workers: list of workers
    address_to_key: dict of public address to private key
    """

    def __init__(self):
        self.workers = []
        self.address_to_key = Helper.read_addresses_and_keys_from_yaml(for_worker=True)

    def create_worker(self):
        """Add a worker to the list of workers (maximum 999 workers as no more addresses)

        Returns: the worker if added, None otherwise
        """
        # check if we don't have created more workers than the number of addresses
        if len(self.workers) < len(self.address_to_key):
            worker = Worker(self.address_to_key[len(self.workers)])
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
