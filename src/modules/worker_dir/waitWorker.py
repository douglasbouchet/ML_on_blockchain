import time
import random


class WaitWorker:
    def __init__(self, address, private_key, id, contract):
        self.address = address
        self.private_key = private_key
        self.contract = contract
        self.id = id

    def get_parameters(self):
        # call the contract to get the parameters
        # TODO
        print("Worker {} get the parameters".format(self.id))
        return

    def fake_learn(self):
        # sleep between 0.1 and 0.3 seconds
        #time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 3))
        print("Worker {} end learning".format(self.id))
        return

    def send_fragment(self, frag_nb):
        print(type(self.contract))
        frag_res = self.contract.add_fragment(
            frag_nb, 1, "0x1234567890", self.address, self.private_key)
        print("Worker {} send fragment result: {}".format(self.id, frag_nb))
        return
