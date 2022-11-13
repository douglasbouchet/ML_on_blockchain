from src.modules.federating_learning_server import FederatingLearningServer
import sys

sys.path.append("/home/user/ml_on_blockchain")

group_size = 3
n_rounds = 100
batch_size = 10


def test_fl_server_should_be_initialized_correctly():
    fl_server = FederatingLearningServer(group_size, n_rounds, batch_size)
    assert fl_server is not None
    # check all arguments of fl_server
    assert fl_server.group_size == group_size
    assert fl_server.n_rounds == n_rounds
    assert fl_server.batch_size == batch_size
    assert fl_server.current_round == 0
    assert fl_server.workers_addresses == []
    assert fl_server.available_workers == []
    # assert fl_server.data is not None
    assert fl_server.address == "fce75e885241b4b465ad8e5919416ad4c9290d3e"
    assert (
        fl_server.private_key
        == "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d"
    )
