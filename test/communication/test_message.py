import sys

sys.path.append("/home/user/ml_on_blockchain")
from src.communication.message import Message


def test_message_content():
    worker_address = "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    model_weight = [1, 2, 3]
    message = Message(worker_address, model_weight)
    assert message.get_worker_address() == worker_address
    assert message.get_model_weight() == model_weight
