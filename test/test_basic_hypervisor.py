import sys

sys.path.append("/home/user/ml_on_blockchain")

from src.basic_server import BasicServer
from src.basic_worker import BasicWorker
from src.modules.helper import Helper
from src.modules.hypervisor import Hypervisor
from src.modules.federating_learning_server import FederatingLearningServer


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


def basic_main():
    # ------Init server and worker--------
    basic_server = init_server()
    basic_worker = create_single_worker()
    # ------Deploy smart contract---------
    # contract = basic_server.deploy("incrementer")
    contract = basic_server.deploy("register")
    print("Initial number of workers:", contract.get_number_of_workers())
    # ------Register worker to server-----
    basic_worker.register_to_learning(contract.contract_address, contract.abi)
    print("current number of workers:", contract.get_number_of_workers())


def test_hypervisor_based_main():
    # ------Init server and hypervisor--------
    # basic_server = init_server()
    learning_server = FederatingLearningServer(3, 100, 10)
    hypervisor = Hypervisor()
    # ------Deploy smart contract---------
    contract = learning_server.deploy_contract("register")
    assert contract.get_number_of_workers() == 0
    # ------Give contract information to hypervisor-----
    hypervisor.set_contract(contract)
    # ------Create some workers-----------
    worker0 = hypervisor.create_worker()
    worker1 = hypervisor.create_worker()
    # ------Register worker to server-----
    hypervisor.make_worker_join_learning(worker0)
    hypervisor.make_worker_join_learning(worker1)
    assert contract.get_number_of_workers() == 2
    # check if learning server has the correct number of workers and their addresses
    server_workers = learning_server.read_worker_from_smart_contract(contract)
    assert len(server_workers) == 2
    assert server_workers[0] == worker0.address
    assert server_workers[1] == worker1.address
    # ------Unregister worker from server-----
    hypervisor.make_worker_leave_learning(worker0)
    assert contract.get_number_of_workers() == 1
    hypervisor.make_worker_leave_learning(worker1)
    assert contract.get_number_of_workers() == 0
    hypervisor.make_worker_leave_learning(worker0)
    assert contract.get_number_of_workers() == 0
