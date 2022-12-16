from src.modules.federating_learning_server import FederatingLearningServer
import sys
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
from web3 import Web3

sys.path.append("/home/user/ml_on_blockchain")


def encode_bytes32(value: str) -> str:
    b = value[2:].encode('utf-8')
    # check if the string is too long
    if len(b)/2 > 32.0:
        raise ValueError("The string is too long to be encoded as bytes32.")
        return None
    # pad the string with 0s
    b += b'\x00' * (32 - len(b))
    return b


def encode_uint(value: int) -> str:
    # if value cannot be represented as uint256, raise an error
    if value < 0 or value > 2**256 - 1:
        raise ValueError("The value cannot be represented as uint256.")
        return None
    return value.to_bytes(32, byteorder='big')


def generate_addresses(n_workers: int):
    """Generate valid ethereum addresses.

    Args:
        n_workers (int): number of addresses to generate
    Returns:
        int[]: the addresses are already converted to int
    """
    addresses = []
    for i in range(n_workers):
        private_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(
            private_key).format(compressed=False)[1:]
        addr = keccak_256(public_key).digest()[-20:]
        addresses.append(int(addr.hex(), 16))
    return addresses


def compute_model_weight(n_workers: int):
    """Generate an array of model weights.

    Args:
        n_workers (int): number of workers

    Returns:
        List[int]: the array of model hashes
    """
    # weights are good(42) for 4/5 of workers and 1/5 of workers are malicious(666)
    return [42 if i % 5 != 0 else 666 for i in range(n_workers)]


def compute_add_new_encrypted_model_hash(n_workers: int, addresses, model_weights):
    """Generate an array of model hashes. Model hashed is obtained by
    adding worker address (as an int) to model weight.

    Args:
        n_workers (int): number of workers
        addresses (int[]): array of worker addresses
        model_weights (int[]): array of model weights

    Returns:
        List[str]: the array of model hashes
    """
    return [Web3.solidityKeccak(["uint256"], [addresses[i] + model_weights[i]]).hex() for i in range(n_workers)]


def test_uint_encoding():
    n_workers = 2
    addresses = generate_addresses(n_workers)
    model_weights = compute_model_weight(n_workers)
    add_new_encrypted_model_arg1 = compute_add_new_encrypted_model_hash(
        n_workers, addresses, model_weights)
    add_new_encryption_model_counter = 0
    add_verification_parameters_counter = 0

    learning_server = FederatingLearningServer(3, 100, 10)
    learn_task = learning_server.deploy_contract(
        "encryptionJobContainer", "EncryptionJobContainer"
    )

    # some original address from yaml file
    yaml_add = "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    # this one was generate by a previous run of the code, but we need the value harcoded in the smart contract
    address_from_generate_addresses = 725016507395605870152133310144839532665846457513
    yaml_add_int = int(yaml_add, 16)
    # check that all addresses are valid
    for i in range(n_workers):
        assert Web3.isAddress(hex(addresses[i]))

    assert Web3.isAddress(hex(addresses[0]))

    assert learn_task.check_address_encoding(
        address_from_generate_addresses) is True

    # checking "addNewEncryptedModel" function
    worker_address = address_from_generate_addresses
    model_hashed_with_address = "0x0a3acd277e8fd4d05446ed4d5d0eeb24e5381a20c7425fbb268461e164f59992"
    print("worker_address: ", worker_address)
    print("model_hashed_with_address: ", model_hashed_with_address)

    assert learn_task.check_uint160_bytes32_encoding(
        worker_address, model_hashed_with_address) is True
    print("all good")
