from src.modules.learning_server import LearningServer
from src.modules.hypervisor import Hypervisor
from src.communication.network import Network
from src.communication.message import Message
from src.modules.helper import Helper
import sys

sys.path.append("/home/user/ml_on_blockchain")


def test_hypervirsor_read_addresses_list_should_be_999_for_workers():
    hypervisor = Hypervisor()
    assert len(hypervisor.address_to_key) == 999


def test_hypervisor_should_start_with_no_workers():
    hypervisor = Hypervisor()
    assert len(hypervisor.address_to_workers) == 0


def test_hypervisor_should_create_worker():
    hypervisor = Hypervisor()
    worker = hypervisor.create_worker()
    assert worker is not None
    assert len(hypervisor.address_to_workers) == 1


def test_hypervisor_should_create_at_most_999_workers():
    # try to create more than 999 workers
    hypervisor = Hypervisor()
    for i in range(1100):
        worker = hypervisor.create_worker()
    assert len(hypervisor.address_to_workers) == 999
    assert hypervisor.create_worker() is None


def test_hypervisor_should_remove_worker():
    # add a worker and remove it
    hypervisor = Hypervisor()
    worker = hypervisor.create_worker()
    assert len(hypervisor.address_to_workers) == 1
    assert hypervisor.remove_worker(worker.address) is not None
    assert len(hypervisor.address_to_workers) == 0

    # create 998 workers and remove them(not 999 as we already created one before, and we can only assign 999 addresses)
    for i in range(998):
        worker = hypervisor.create_worker()
        assert hypervisor.remove_worker(worker.address) is not None
    assert len(hypervisor.address_to_workers) == 0


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


def test_handle_messages_should_update_model_weigths_only_specfifed_workers():
    hypervisor = Hypervisor()
    worker1 = hypervisor.create_worker()
    worker2 = hypervisor.create_worker()
    learning_server = LearningServer(
        "public_address", "private_key"
    )  # no need to give correct ids for this test

    # create a network
    network = Network(hypervisor, learning_server)

    # create a message with the new weights
    new_weights = [1, 2, 3, 4, 5]
    msg = Message(worker1.address, new_weights)

    # send the message to the hypervisor
    assert network.send_message(msg, hypervisor.ip_address) == True

    # handle the message
    hypervisor.handle_messages(network)

    # verify that weights of worker1 are updated but not worker2
    assert worker1.model_weights == new_weights
    assert worker2.model_weights is None


def test_hypevisor_should_correctly_create_mnist_worker():
    hypervisor = Hypervisor()
    mnist_worker = hypervisor.create_mnist_worker()
    assert mnist_worker is not None
    assert len(hypervisor.address_to_workers) == 1
    assert mnist_worker.address == "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    assert (
        mnist_worker.private_key
        == "9793a9cb6042ef94219797af47062b38100e535fdb7034a2ae9ba4136a6d17b4"
    )
