import solcx


def compile_smart_contract(contract_name):
    """Compile smart contract using solcx and return its abi and bytecode

    Args:
        contract_name (str): Name of the contract to compile.

    Returns:
        string, string: ABI and bytecode of smart contract.
    """
    temp_file = solcx.compile_files(
        f"/home/user/ml_on_blockchain/smart-contracts/{contract_name}.sol"
    )

    abi = temp_file[
        f"/home/user/ml_on_blockchain/smart-contracts/{contract_name}.sol:{contract_name.capitalize()}"
    ]["abi"]
    bytecode = temp_file[
        f"/home/user/ml_on_blockchain/smart-contracts/{contract_name}.sol:{contract_name.capitalize()}"
    ]["bin"]

    return abi, bytecode
