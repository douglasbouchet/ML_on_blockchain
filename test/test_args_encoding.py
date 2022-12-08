from src.modules.federating_learning_server import FederatingLearningServer
from src.solidity_contract.encode_args import encode_uint160_as_function_call, encode_uint256_as_function_call, encode_bool_as_function_call, encode_bytes32_as_function_call, encode_args_as_function_call
import sys

sys.path.append("/home/user/ml_on_blockchain")


def test_uint160_encoding():
    value = 69
    # this is expecected value for uint160
    true_value = "0x0000000000000000000000000000000000000000000000000000000000000045"
    encoded_value = encode_uint160_as_function_call(value)
    assert encoded_value == true_value
    value = 6518
    # this is expecected value for uint160
    true_value = "0x0000000000000000000000000000000000000000000000000000000000001976"
    encoded_value = encode_uint160_as_function_call(value)
    assert encoded_value == true_value
    # generate the maximum value for uint160
    value = 2 ** 160 - 1
    # this is expecected value for uint160
    true_value = "0x000000000000000000000000ffffffffffffffffffffffffffffffffffffffff"
    encoded_value = encode_uint160_as_function_call(value)
    assert encoded_value == true_value


def test_uint256_encoding():
    value = 69
    # this is expecected value for uint256
    true_value = "0x0000000000000000000000000000000000000000000000000000000000000045"
    encoded_value = encode_uint256_as_function_call(value)
    assert encoded_value == true_value


def test_bool_encoding():
    value = True
    # this is expecected value for true bool
    true_value = "0x0000000000000000000000000000000000000000000000000000000000000001"
    encoded_value = encode_bool_as_function_call(value)
    assert encoded_value == true_value
    value = False
    # this is expecected value for false bool
    true_value = "0x0000000000000000000000000000000000000000000000000000000000000000"
    encoded_value = encode_bool_as_function_call(value)
    assert encoded_value == true_value


def test_bytes32_encoding():
    # generate a bytes string of length 32
    value = "a" * 32
    # generate me a string of length 32 consisting of 0x61
    true_value = "0x" + "61" * 32
    encoded_value = encode_bytes32_as_function_call(value)
    assert encoded_value == true_value


def test_encode_args_as_function_call():
    # this should correctly encode multiple arguments
    # start with simple uint160, then uint160
    args = [69, 420]
    true_value = "0x0000000000000000000000000000000000000000000000000000000000000045"
    true_value += "00000000000000000000000000000000000000000000000000000000000001a4"
    # encode each argument separately
    args = [encode_uint160_as_function_call(arg) for arg in args]
    encoded_value = encode_args_as_function_call(args)
    assert encoded_value == true_value
    # check uint32,bool with (69, True)
    args = [69, True]
    true_value = "0x0000000000000000000000000000000000000000000000000000000000000045"
    true_value += "0000000000000000000000000000000000000000000000000000000000000001"
    # encode each argument separately
    arg0 = encode_uint256_as_function_call(args[0])
    arg1 = encode_bool_as_function_call(args[1])
    args = [arg0, arg1]
    encoded_value = encode_args_as_function_call(args)
    assert encoded_value == true_value
