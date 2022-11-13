import time


class WaitWorker:
    def __init__(self, address, private_key):
        self.address = address
        self.private_key = private_key

    def fake_learn(self):
        # sleep between 0.1 and 0.3 seconds
        time.sleep(random.uniform(0.1, 0.3))
        return
