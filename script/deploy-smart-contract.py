from web3 import Web3

# connect to one of the local quorum blockchain node
web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
web3 = Web3(Web3.WebsocketProvider("ws://192.168.203.4:9000"))
print(web3.isConnected())


# print(w3.eth.get_block("latest"))

print(web3.eth.accounts)

print(web3.eth.protocol_version)


print(web3.toChecksumAddress("0xfce75e885241b4b465ad8e5919416ad4c9290d3e"))
# print(web3.eth.get_balance("0xfce75e885241b4b465ad8e5919416ad4c9290d3e"))
print(
    web3.eth.get_balance(
        web3.toChecksumAddress("0xfce75e885241b4b465ad8e5919416ad4c9290d3e")
    )
)
