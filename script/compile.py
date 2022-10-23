# 1. Import solcx
import solcx

# # 2. If you haven't already installed the Solidity compiler, uncomment the following line
# # solcx.install_solc()

# # 3. Compile contract
# # temp_file = solcx.compile_files('../smart-contracts/Incrementer.sol')
# temp_file = solcx.compile_files(
#     "/home/user/ml-on-blockchain/smart-contracts/incrementer.sol"
# )

# # 4. Export contract data
# # abi = temp_file['Incrementer.sol:Incrementer']['abi']
# abi = temp_file[
#     "/home/user/ml-on-blockchain/smart-contracts/incrementer.sol:Incrementer"
# ]["abi"]
# bytecode = temp_file[
#     "/home/user/ml-on-blockchain/smart-contracts/incrementer.sol:Incrementer"
# ]["bin"]


def compile_smart_contract(contract_name):
    """Compile smart contract using solcx.

    Args:
        contract_name (str): Name of the contract to compile.

    Returns:
        dict: Compiled smart contract.
    """
    temp_file = solcx.compile_files(
        f"/home/user/ml-on-blockchain/smart-contracts/{contract_name}.sol"
    )


def get_abi(contract_name):
    """Get ABI of smart contract.
    Require to compile smart contract first.

    Args:
        contract_name (str): Name of the contract to compile.

    Returns:
        dict: ABI of smart contract.
    """
    return temp_file[
        f"/home/user/ml-on-blockchain/smart-contracts/{contract_name}.sol:{contract_name}"
    ]["abi"]


def get_bytecode(contract_name):
    """Get bytecode of smart contract.
    Require to compile smart contract first.

    Args:
        contract_name (str): Name of the contract to compile.

    Returns:
        dict: Bytecode of smart contract.
    """
    return temp_file[
        f"/home/user/ml-on-blockchain/smart-contracts/{contract_name}.sol:{contract_name}"
    ]["bin"]
