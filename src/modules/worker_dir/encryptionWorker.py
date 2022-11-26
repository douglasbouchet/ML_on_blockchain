import random
from web3 import Web3
from web3.auto import w3


class EncryptionWorker:
    def __init__(self, address, private_key, id, contract):
        self.address = address
        self.private_key = private_key
        self.contract = contract
        self.id = id
        self.nounce = self.generate_nounce()
        self.secret = self.generate_secret()

        # send_encrypted_model
        # get_number_submitted_models
        # send_verifications_parameters

    def generate_nounce(self):
        # TODO
        return random.randint(0, 100)

    def generate_secret(self):
        # TODO
        # generate a bit string of length 32
        secret = [1 for i in range(32)]
        return secret

    def encrypt_model(self, model):
        # TODO
        # encrypt the model with the secret
        # xor the model with the secret
        encrypted_model = [model[i] ^ self.secret[i]
                           for i in range(len(model))]
        # convert encrypted_model to bytes TODO see if necessary
        # encrypted_model = bytes(encrypted_model)
        return encrypted_model

    def send_encrypted_model(self):
        # learn a model
        model = self.learn_model()
        #print("model", model)
        # encrypt the model
        encrypted_model = self.encrypt_model(model)
        #print("encrypted_model", encrypted_model)
        encrypted_model = "".join([str(i) for i in encrypted_model])
        #print("encrypted_model", encrypted_model)
        # convert the encrypted model a bite array
        #encrypted_model = bytes(encrypted_model, 'utf-8')
        encrypted_model = bytes('1111', 'utf-8')
        # convert the model to hexadecimals
        #encrypted_model_hex = Web3.toHex(encrypted_model)
        #print("encrypted_model", encrypted_model)
        res = self.contract.send_encrypted_model(
            encrypted_model, self.address, self.private_key
        )
        if (res[0] == True and res[1] == True):
            #print("model sent")
            return True
        else:
            #print("model not sent")
            return False

    def check_can_send_verification_parameters(self):
        # check the number of submitted models from the smart contract
        return self.contract.check_can_send_verification_parameters()

    def send_veritications(self):
        # send the verifications to the blockchain (self.nounce, self.secret)
        # TODO replace secret by full length
        self.contract.send_verifications_parameters(
            self.nounce, bytes(self.secret)[:4], self.address, self.private_key
        )

    def learn_model(self):
        # TODO
        # generate a 32 bit array of 0s
        model = [0 for i in range(32)]
        return model
