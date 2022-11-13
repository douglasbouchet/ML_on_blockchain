import time
import random


class WaitWorker:
    def __init__(self, address, private_key, id):
        self.address = address
        self.private_key = private_key
        self.id = id

    def fake_learn(self):
        # sleep between 0.1 and 0.3 seconds
        #time.sleep(random.uniform(0.1, 0.3))
        time.sleep(random.uniform(1, 3))
        print("Worker {} end learning".format(self.id))
        return
