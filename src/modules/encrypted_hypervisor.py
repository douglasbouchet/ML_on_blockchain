from web3 import Web3
from src.modules.helper import Helper
from src.modules.worker_dir.encryptionWorker import EncryptionWorker


# new hypervisor which facilitate interactions with worker
# method to load contracts (should be called everytime a worker wants to join)
# method to send new model to the contract (should timeout some scnds to simulate computation and send the model)
# this method also handle the case where the weights are not accepted by the contract <- see how we implement this


class EncryptedHypervisor:
    def __init__(self):
        self.address_to_workers = {}  # dict of address to worker
        self.address_to_key = Helper.read_addresses_and_keys_from_yaml(
            Helper, for_worker=True
        )
        self.address_used = []  # usefull as we don't want to use the same address twice
        self.contract = None
        self.workers = []

    def create_encrypted_workers(self, number_of_workers):
        """Add a worker to the list of workers (maximum 999 workers as no more addresses)"""
        # check if we don't have created more workers than the number of addresses
        for i in range(number_of_workers):
            if len(self.address_used) < len(self.address_to_key):
                address_and_key = self.address_to_key[len(self.address_used)]
                self.address_used.append(address_and_key["address"])
                worker = EncryptionWorker(
                    address_and_key["address"],
                    address_and_key["private"],
                    i,
                    self.contract,
                )
                self.address_to_workers[worker.address] = worker
                self.workers.append(worker)

    def select_worker_pool(self, pool_size):
        """Select a pool of workers to use for the learning

        Args:
            pool_size (int): the size of the pool to select
        Returns: the list of workers selected
        """
        if pool_size > len(self.workers):
            print("Not enough workers to create a pool of size {}".format(pool_size))
            return
        # select pool_size workers randomly
        # pool = random.sample(self.workers, pool_size)
        pool = self.workers[:pool_size]
        return pool
