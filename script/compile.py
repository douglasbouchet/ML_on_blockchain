# 1. Import solcx
import solcx

# 2. If you haven't already installed the Solidity compiler, uncomment the following line
# solcx.install_solc()

# 3. Compile contract
# temp_file = solcx.compile_files('../smart-contracts/Incrementer.sol')
temp_file = solcx.compile_files(
    "/home/user/ml-on-blockchain/smart-contracts/incrementer.sol"
)

# 4. Export contract data
# abi = temp_file['Incrementer.sol:Incrementer']['abi']
abi = temp_file[
    "/home/user/ml-on-blockchain/smart-contracts/incrementer.sol:Incrementer"
]["abi"]
bytecode = temp_file[
    "/home/user/ml-on-blockchain/smart-contracts/incrementer.sol:Incrementer"
]["bin"]
