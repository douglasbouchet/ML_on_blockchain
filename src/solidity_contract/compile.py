import solcx


def compile_smart_contract(contract_file_name, contract_name):
    """Compile smart contract using solcx and return its abi and bytecode

    Args:
        contract_name (str): Name of the contract to compile.

    Returns:
        string, string: ABI and bytecode of smart contract.
    """
    solcx.install_solc(version="0.7.0")
    solcx.set_solc_version("0.7.0")
    temp_file = solcx.compile_files(
        # f"/home/user/ml_on_blockchain/smart-contracts/{contract_name}.sol"
        f"/home/user/ml_on_blockchain/smart-contracts/{contract_file_name}.sol"
    )

    # filename:contract_name"
    abi = temp_file[
        f"/home/user/ml_on_blockchain/smart-contracts/{contract_file_name}.sol:{contract_name}"
    ]["abi"]
    bytecode = temp_file[
        f"/home/user/ml_on_blockchain/smart-contracts/{contract_file_name}.sol:{contract_name}"
    ]["bin"]

    return abi, bytecode
