import time
import random
from web3 import Web3
from web3.auto import w3


class WaitWorker:
    def __init__(self, address, private_key, id, contract):
        self.address = address
        self.private_key = private_key
        self.contract = contract
        self.id = id

    def get_parameters(self):
        """Load a contract to use for the learning.
        The parameters are getted from the blockchain. We don't make a single call as we want the behavior to be
        as realistic as possible. I.e in a real system, we assume each workers will independently get the parameters.
        We can in consequence parallelize the calls to the blockchain.

        This method will be called in parallel by each worker of the pool
        """
        # call the contract to get the parameters
        print("Worker {} get the parameters".format(self.id))
        return

    def fake_learn(self):
        # sleep between 0.1 and 0.3 seconds
        # time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 3))
        print("Worker {} end learning".format(self.id))
        return

    def send_fragment(self, frag_nb):
        # frag_res = self.contract.add_fragment(
        #    frag_nb, 1, "0x1234567890", self.address, self.private_key)
        # print("Worker {} send fragment result: {}".format(self.id, frag_nb))
        (boolean, msg) = self.contract.add_fragment(
            frag_nb, 1, "0x1234567890", self.address, self.private_key)
        #print("Worker {} send fragment".format(self.id))
        print("Worker {} send fragment result: {}:{}".format(self.id, boolean, msg))
        return

    def print_latest_block(self):
        web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
        print("web3 connected: {}".format(web3.isConnected()))
        # print("Latest Ethereum block number", w3.eth.block)
        return
