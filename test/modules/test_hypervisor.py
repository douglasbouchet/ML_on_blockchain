import sys

sys.path.append("/home/user/ml_on_blockchain")
from src.modules.helper import Helper
from src.modules.hypervisor import Hypervisor


def test_hypervirsor_read_addresses_list_should_be_999_for_workers():
    hypervisor = Hypervisor()
    assert len(hypervisor.address_to_key) == 999


def test_hypervisor_should_start_with_no_workers():
    hypervisor = Hypervisor()
    assert len(hypervisor.workers) == 0


def test_hypervisor_should_create_worker():
    hypervisor = Hypervisor()
    worker = hypervisor.create_worker()
    assert worker is not None
    assert len(hypervisor.workers) == 1


def test_hypervisor_should_create_at_most_999_workers():
    # try to create more than 999 workers
    hypervisor = Hypervisor()
    for i in range(1100):
        worker = hypervisor.create_worker()
    assert len(hypervisor.workers) == 999
    assert hypervisor.create_worker() is None


def test_hypervisor_should_remove_worker():
    # add a worker and remove it
    hypervisor = Hypervisor()
    worker = hypervisor.create_worker()
    assert len(hypervisor.workers) == 1
    assert hypervisor.remove_worker(worker.address) is not None
    assert len(hypervisor.workers) == 0

    # create 999 workers and remove them
    for i in range(999):
        worker = hypervisor.create_worker()
        assert hypervisor.remove_worker(worker.address) is not None
    assert len(hypervisor.workers) == 0


def test_hypervisor_should_not_remove_worker_if_not_found():
    hypervisor = Hypervisor()
    assert hypervisor.remove_worker("fake_address") is None


def test_hypervisor_should_create_workers_with_correct_address_and_key():
    hypervisor = Hypervisor()
    worker = hypervisor.create_worker()
    assert worker.address == "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    assert (
        worker.private_key
        == "9793a9cb6042ef94219797af47062b38100e535fdb7034a2ae9ba4136a6d17b4"
    )
    worker = hypervisor.create_worker()
    assert worker.address == "412000cd0add0d3ed0a2ae686335e588651a1f9a"
    assert (
        worker.private_key
        == "c43ef4a23b5967099b91adb3a155b14f816e72840b50ff39629b7f263a3dc312"
    )
    worker = hypervisor.create_worker()
    assert worker.address == "197fc3dccac87b7546a9223cc445b4f594a2e3e7"
    assert (
        worker.private_key
        == "a1ab7278965cb9d311093f8c96ade50f998569d4f74941ff923d1cc512492f6b"
    )


# def make_worker_join_learning(self, worker):
#         """Make a worker participate to the learning

#         Args:
#             worker (Worker): the worker to make participate to the learning
#         """
#         # if contract abi and addresses aren't available do nothing
#         if self.contract is None:
#             print(
#                 "No contract found, please deploy a contract first"
#             )
#             return
#         worker.register_to_learning(self.contract.contract_address, self.contract.abi)

#     def set_contract(self, contract):
#         """Set the contract to use for the learning

#         Args:
#             contract (Contract): the contract to use for the learning
#         """
#         assert type(contract) == Contract
#         self.contract = contract
