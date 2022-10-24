from src.basic_server import BasicServer
from src.basic_worker import BasicWorker


def init_server():
    server_address = "fce75e885241b4b465ad8e5919416ad4c9290d3e"
    server_private_key = (
        "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d"
    )
    basic_server = BasicServer(server_address, server_private_key)
    return basic_server


def create_single_worker():
    worker_address = "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    worker_private_key = (
        "9793a9cb6042ef94219797af47062b38100e535fdb7034a2ae9ba4136a6d17b4"
    )
    basic_worker = BasicWorker(worker_address, worker_private_key)
    return basic_worker


def main():
    # ------Init server and worker--------
    basic_server = init_server()
    basic_worker = create_single_worker()
    # ------Deploy smart contract---------
    contract = basic_server.deploy()
    print("Initial number of workers:", contract.get_number_of_workers())
    # ------Register worker to server-----
    basic_worker.register_to_learning(contract.contract_address, contract.abi)
    print("current number of workers:", contract.get_number_of_workers())


if __name__ == "__main__":
    main()
