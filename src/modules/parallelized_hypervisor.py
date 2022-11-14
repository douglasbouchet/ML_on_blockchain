import random
from web3 import Web3
from multiprocessing import Process
from src.modules.helper import Helper
from src.modules.worker_dir.waitWorker import WaitWorker


# new hypervisor which facilitate interactions with worker
# method to load contracts (should be called everytime a worker wants to join)
# method to send new model to the contract (should timeout some scnds to simulate computation and send the model)
# this method also handle the case where the weights are not accepted by the contract <- see how we implement this


class ParallelizedHypervisor:
    def __init__(self):
        self.address_to_workers = {}  # dict of address to worker
        self.address_to_key = Helper.read_addresses_and_keys_from_yaml(
            Helper, for_worker=True
        )
        self.address_used = []  # usefull as we don't want to use the same address twice
        self.contract = None
        self.workers = []

    def create_wait_workers(self, number_of_workers):
        """Add a worker to the list of workers (maximum 999 workers as no more addresses)"""
        # check if we don't have created more workers than the number of addresses
        for i in range(number_of_workers):
            if len(self.address_used) < len(self.address_to_key):
                address_and_key = self.address_to_key[len(self.address_used)]
                self.address_used.append(address_and_key["address"])
                worker = WaitWorker(
                    address_and_key["address"], address_and_key["private"], i, self.contract)
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
        #pool = random.sample(self.workers, pool_size)
        pool = self.workers[:pool_size]
        return pool

    def learn(self, worker):
        """Learn the model with the parameters getted from the blockchain
        Actually this is just a random time sleep to simulate the learning

        Args:
            worker (Worker): the worker that will learn the model
        """
        # sleep between 0.1 and 0.3 seconds
        worker.fake_learn()
        return

    def send_weights(self, worker, weights, web3):
        """Send the weights to the blockchain

        Args:
            worker (Worker): the worker that will send the weights
            weights (list): the weights to send
        Returns: True if the weights are accepted, False otherwise
        """
        # call the contract to send the weights and handle the response
        # TODO
        # worker.send_fragment(1)
        print("Worker {} send the weights".format(worker.id))
        return True

    def perform_get_weights(self, workers):
        """Perform the get weights step for each given worker

        Args:
            workers (list): the list of workers to perform the step
        """
        # permute the workers to get a random order
        rmd_ord_workers = random.sample(workers, len(workers))
        for worker in rmd_ord_workers:
            worker.get_parameters()
        return

    def perform_parallel_fake_learn(self, workers):
        """Perform the get weights step for each given worker

        Args:
            workers (list): the list of workers to perform the step
        """
        # permute the workers to get a random order
        processes = [Process(target=self.learn, args=(worker,))
                     for worker in workers]
        self.perform_one_process_step(processes)
        return

    def perform_send_fragment(self, workers):
        """Perform the get weights step for each given worker

        Args:
            workers (list): the list of workers to perform the step
        """
        # permute the workers to get a random order
        # permute the workers to get a random order
        rmd_ord_workers = random.sample(workers, len(workers))
        for worker in rmd_ord_workers:
            worker.send_fragment(1)
        return

    def create_get_weights_process(self, workers):
        """Create a process which will get the weights from the blockchain for each given worker

        Returns: the process created
        """
        process = [Process(target=self.get_weights, args=(worker,))
                   for worker in workers]
        return process

    def create_fake_learn_process(self, workers):
        """Create a process which will learn the model for each given worker

        Returns: the process created
        """
        process = [Process(target=self.learn, args=(worker,))
                   for worker in workers]
        return process

    def create_send_weights_process(self, workers):
        """Create a process which will send the weights to the blockchain for each given worker

        Returns: the process created
        """
        dumb_weight = 1
        web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
        process = [Process(target=self.send_weights, args=(worker, dumb_weight, web3,))
                   for worker in workers]
        return process

    def perform_one_process_step(self, processes):
        """Perform one step of the process

        Args:
            processes (list): the list of processes to perform
        """
        for process in processes:
            process.start()
        for process in processes:
            process.join()
