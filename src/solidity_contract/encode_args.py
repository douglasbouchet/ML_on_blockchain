from eth_abi import encode


def conv_from_bytes_array_to_hex_string(bytes_array: bytes) -> str:
    """
    Convert a bytes array to a hex string.
    :param bytes_array: The bytes array to convert.
    :return: The hex string.
    """
    hex_string = "0x"
    for i in range(len(bytes_array)):
        hex_string += hex(bytes_array[i])[2:].zfill(2)
    return hex_string


def encode_uint160_as_function_call(value: int) -> str:
    # Encode the function call and return the result
    encoded = encode(['uint160'], [value])
    return conv_from_bytes_array_to_hex_string(encoded)


def encode_uint256_as_function_call(value: int) -> str:
    # Encode the function call and return the result
    encoded = encode(['uint256'], [value])
    return conv_from_bytes_array_to_hex_string(encoded)


def encode_bool_as_function_call(value: bool) -> str:
    # Encode the function call and return the result
    encoded = encode(['bool'], [value])
    return conv_from_bytes_array_to_hex_string(encoded)


def encode_bytes32_as_function_call(value: str) -> str:
    # Encode the function call and return the result
    encoded = encode(['bytes32'], [value.encode('utf-8')])
    return conv_from_bytes_array_to_hex_string(encoded)


def encode_args_as_function_call(args: list) -> str:
    """
    Encode the arguments as a function call.
    :param args: The arguments to encode.
        They should start with 0x and be in hex format.
    :return: The encoded function call.
    """
    final_encoding = "0x"
    # concatenate each element of the list and remove the leading 0x
    for arg in args:
        final_encoding += arg[2:]
    return final_encoding
