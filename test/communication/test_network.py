from src.modules.learning_server import LearningServer
from src.modules.hypervisor import Hypervisor
from src.communication.network import Network
from src.communication.message import Message
import sys

sys.path.append("/home/user/ml_on_blockchain")

hypervisor = Hypervisor()
workers = [hypervisor.create_worker() for i in range(100)]
server_address = "fce75e885241b4b465ad8e5919416ad4c9290d3e"
server_private_key = "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d"
learning_server = LearningServer(server_address, server_private_key)


def test_network_should_have_correct_ip_addresses():
    network = Network(hypervisor, learning_server)
    assert len(network.msg_box) == 2
    assert hypervisor.ip_address in network.msg_box
    assert learning_server.ip_address in network.msg_box


def test_network_should_init_with_no_msg():
    network = Network(hypervisor, learning_server)
    assert len(network.msg_box[hypervisor.ip_address]) == 0
    assert len(network.msg_box[learning_server.ip_address]) == 0


def test_network_send_message_should_return_true_if_msg_sent():
    network = Network(hypervisor, learning_server)
    msg = Message(workers[0].address, [1, 2, 3])
    assert network.send_message(msg, learning_server.ip_address) == True


def test_network_send_message_should_return_false_if_msg_not_sent():
    network = Network(hypervisor, learning_server)
    msg = Message(workers[0].address, [1, 2, 3])
    assert network.send_message(msg, "some invalid ip address") == False


def test_network_read_messages_should_return_messages():
    network = Network(hypervisor, learning_server)
    msg = Message(workers[0].address, [1, 2, 3])
    network.send_message(msg, learning_server.ip_address)
    message = network.read_messages(learning_server.ip_address)
    assert len(message) == 1
    assert message[0].get_worker_address() == workers[0].address
    assert message[0].get_model_weight() == [1, 2, 3]


def test_network_read_messages_should_return_none_if_invalid_ip_address():
    network = Network(hypervisor, learning_server)
    message = network.read_messages("some invalid ip address")
    assert message == None


def test_network_read_messages_should_clear_messages():
    network = Network(hypervisor, learning_server)
    msg = Message(workers[0].address, [1, 2, 3])
    network.send_message(msg, learning_server.ip_address)
    message = network.read_messages(learning_server.ip_address)
    assert len(message) == 1
    message = network.read_messages(learning_server.ip_address)
    assert message == []


def test_network_send_message_elaborate_case():
    network = Network(hypervisor, learning_server)
    # send messages from all workers to learning server
    for i in range(len(workers)):
        msg = Message(workers[i].address, [1, 2, 3])
        network.send_message(msg, learning_server.ip_address)
    # check that all messages have been sent
    assert len(network.msg_box[learning_server.ip_address]) == len(workers)
    # read messages from learning server
    messages = network.read_messages(learning_server.ip_address)
    # check that all messages have been correctly read
    assert len(messages) == len(workers)
    for message in messages:
        assert message.get_worker_address(
        ) in [worker.address for worker in workers]
        assert message.get_model_weight() == [1, 2, 3]
    # check that all messages have been correctly deleted
    assert len(network.msg_box[learning_server.ip_address]) == 0
