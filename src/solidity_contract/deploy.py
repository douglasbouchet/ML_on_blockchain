from web3 import Web3
#from web3.middleware import pythonic_middleware, attrdict_middleware
from web3.middleware import geth_poa_middleware
from web3 import middleware
from eth_account import Account
from src.solidity_contract.compile import compile_smart_contract


def deploy_smart_contract(
    contract_file_name, contract_name, from_address, from_private_key
):
    # 2. Add the Web3 provider logic here:
    w3 = Web3(Web3.WebsocketProvider("ws://192.168.203.6:9000"))
    # w3 = Web3(Web3.WebsocketProvider("ws://192.168.201.5:9000"))
    #w3 = Web3(Web3.WebsocketProvider("ws://192.168.203.4:9000"))
    # w3 = Web3(Web3.WebsocketProvider("ws://192.168.203.3:9000"))
    print("w3 connected: {}".format(w3.isConnected()))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # 3. Create address variable
    account_from = {
        "private_key": from_private_key,
        "address": from_address,
    }

    print(f'Attempting to deploy from account: { account_from["address"] }')

    # get abi and bytecode from compiled contract
    abi, bytecode = compile_smart_contract(contract_file_name, contract_name)

    new_contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # 5. Build constructor tx
    # construct_txn = new_contract.constructor(5).buildTransaction(
    construct_txn = new_contract.constructor().buildTransaction(  # TODO modify here the syntax of constructor depending on the smart contract
        {
            "chainId": w3.eth.chainId,
            "gas": 0,
            "gasPrice": w3.eth.gasPrice,
            "from": Web3.toChecksumAddress(account_from["address"]),
            "nonce": w3.eth.get_transaction_count(
                Web3.toChecksumAddress(account_from["address"])
            ),
        }
    )
    gas = w3.eth.estimate_gas(construct_txn)
    print('Estimated gas: ', gas)
    construct_txn.update({'gas': gas})

    # 6. Sign tx with PK
    tx_create = w3.eth.account.sign_transaction(
        construct_txn, account_from["private_key"]
    )
    # 7. Send tx and wait for receipt
    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
    print('tx sent')
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Contract deployed at address: { tx_receipt.contractAddress }")
    return tx_receipt.contractAddress, abi, bytecode
