import random
from web3 import Web3
from web3.auto import w3


class EncryptionWorker:
    def __init__(self, address, private_key, id, contract):
        self.address = address
        self.private_key = private_key
        self.contract = contract
        self.id = id
        self.r = self.generate_r()
        self.secret = self.generate_secret()

    def generate_r(self):
        # TODO
        return random.randint(0, 100)

    def generate_secret(self):
        # generate a string of length 32 from r
        # TODO
        return str(self.r).zfill(32)

    def encrypt_model(self, model):
        # encrypt the model with the secret
        # TODO
        return model

    def send_encrypted_model(self, encrypted_model):
        # send the encrypted model to the blockchain
        # TODO
        pass

    def check_n_submitted_models(self):
        # check the number of submitted models from the smart contract
        # TODO
        return -1

    def send_veritications(self):
        # send the verifications to the blockchain (self.r, self.secret)
        # TODO
        pass
