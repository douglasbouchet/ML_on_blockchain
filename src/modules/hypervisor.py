from worker import Worker


class Hypervisor:
    """Manage the workers in order to perform distributed learning
    Contains method to add new workers, make them participate into learning or stop participating
    to the learning

    workers: list of workers
    address_to_key: dict of public address to private key
    """

    def __init__(self):
        self.workers = []
        self.address_to_key = {}

    def create_worker(self):
        """Add a worker to the list of workers

        Args:
            worker (Worker): The worker to add

        """
        worker = Worker()
        self.workers.append(worker)

    def read_addresses_and_keys_from_file(self, file_path):
        """Get the addresses and keys of the workers

        Returns:
            dict: The dict of addresses and keys
        """
        return self.address_to_key
