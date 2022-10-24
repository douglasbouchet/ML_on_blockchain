from web3 import Web3
from compile import abi

web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
print("web3 connected: {}".format(web3.isConnected()))

contract_address = (
    "0x641b0cf8B4685589C8DC18c79006585268783c15"  # depending on result of deploy.py
)

print(f"Making a call to contract at address: { contract_address }")

# 4. Create contract instance
Incrementer = web3.eth.contract(address=contract_address, abi=abi)

# 5. Call Contract
number = Incrementer.functions.number().call()

print(f"The current number stored is: { number } ")
