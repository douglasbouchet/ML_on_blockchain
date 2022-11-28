import sha3
import os
from web3 import Web3
from web3.auto import w3


class EncryptionWorker:
    def __init__(self, address, private_key, id, contract):
        self.address = address
        self.private_key = private_key
        self.contract = contract
        self.id = id
        # key used for model encryption and verification. Should be used once for each model
        self.secret = self.generate_secret()
        #self.secret = Fernet.generate_key()
        self.k = sha3.keccak_256()

    def generate_secret(self) -> bytes:
        """Generate a secret key for the worker
        The secret key consists of 32 random bytes
        Returns:
            bytes: secret key
        """
        # generate a random 32 bytes array
        return os.urandom(32)

    def encrypt_model(self, model) -> bytes:
        """Encrypt the model using the secret key
        Model xored with secret as a byte array of size 32.
        Then compute its Keccak256 hash
        Args:
            model(int[32]): model to encrypt

        return:
        """
        print("secret", self.secret)
        # convert the model to a byte array
        model_bytes = bytes(model)
        # xor the model using the secret
        encrypted_model = bytes(
            [a ^ b for a, b in zip(model_bytes, self.secret)])
        # compute the keccak256 hash of the encrypted model
        self.k.update(encrypted_model)
        return self.k.digest()

    def send_encrypted_model(self, good_model=True):
        # First we compute the model
        model = self.learn_model(good_model)
        # compute the keccak hash of the model
        self.k.update(bytes(model))
        model_keccak = self.k.digest()
        # encrypt the model using Fernet and the worker's secret
        model_secret_keccak = self.encrypt_model(model)  # bytes[64]
        print("encrypted_model", model_secret_keccak)
        print(type(model_secret_keccak))
        res = self.contract.send_encrypted_model(
            model_keccak, model_secret_keccak, self.address, self.private_key
        )
        if len(res) == 2:
            return (res[0] == True and res[1] == True)
        return False
    # def send_encrypted_model(self, good_model=True):
    #     model = self.learn_model(good_model)
    #     # encrypt the model using Fernet and the worker's secret
    #     encrypted_model = self.encrypt_model(model)
    #     #print("encrypted_model", encrypted_model)
    #     encrypted_model = "".join([str(i) for i in encrypted_model])
    #     #print("encrypted_model", encrypted_model)
    #     # convert the encrypted model a bite array
    #     #encrypted_model = bytes(encrypted_model, 'utf-8')
    #     encrypted_model = bytes('1111', 'utf-8')
    #     # convert the model to hexadecimals
    #     #encrypted_model_hex = Web3.toHex(encrypted_model)
    #     #print("encrypted_model", encrypted_model)
    #     res = self.contract.send_encrypted_model(
    #         encrypted_model, self.address, self.private_key
    #     )
    #     if len(res) == 2:
    #         return (res[0] == True and res[1] == True)
    #     return False

    def check_can_send_verification_parameters(self):
        # check the number of submitted models from the smart contract
        return self.contract.check_can_send_verification_parameters()

    # def send_verifications(self):
    #     # send the verifications to the blockchain (self.nounce, self.secret)
    #     # TODO replace secret by full length
    #     return self.contract.send_verifications_parameters(
    #         #self.nounce, bytes(self.secret)[:4], self.address, self.private_key
    #         0, bytes("sdsdsdsd".encode())[:4], self.address, self.secret
    #     )
    def send_verifications(self, good_model=True) -> bool:
        clear_secret = self.secret
        clear_model = self.learn_model(good_model)
        # convert the model to a byte array
        clear_model_bytes = bytes(clear_model)
        return self.contract.send_verifications_parameters(
            clear_secret, clear_model_bytes, self.address, self.private_key
        )

    def learn_model(self, good_model=True):
        """Learn a new model
        This method is really simple and just returns a simple array of int

        Args:
            good_model (bool, optional): _description_. Defaults to True.

        Returns:
            str: [1]*32 if good_model is true [0]*32 otherwise
        """
        if good_model:
            return [1 for i in range(32)]
        else:
            return [0 for i in range(32)]
        # TODO
        # generate a 32 bit array of 0s
        #model = [0 for i in range(32)]
        # return model
