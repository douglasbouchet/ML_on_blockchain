from src.modules.helper import Helper
import sys

sys.path.append("/home/user/ml_on_blockchain")


def test_read_addresses_list_should_be_999_for_workers():
    assert (
        len(Helper().read_addresses_and_keys_from_yaml(Helper(), for_worker=True))
        == 999
    )
    assert (
        len(Helper().read_addresses_and_keys_from_yaml(
            Helper(), for_worker=False)) == 1
    )


def test_read_addresses_and_keys_from_yaml_should_return_correct_value():
    worker_addresses = Helper().read_addresses_and_keys_from_yaml(
        Helper(), for_worker=True
    )
    server_addresse = Helper().read_addresses_and_keys_from_yaml(
        Helper(), for_worker=False
    )
    assert worker_addresses[0]["address"] == "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    assert (
        worker_addresses[0]["private"]
        == "9793a9cb6042ef94219797af47062b38100e535fdb7034a2ae9ba4136a6d17b4"
    )
    assert worker_addresses[3]["address"] == "85c91093b4301816fbc4a52bf2e4c126a9146a24"
    assert (
        worker_addresses[3]["private"]
        == "2b7264914d1eecaa76d7829755ccdac9a50db16466068ee8b561e66ed249d9a5"
    )
    assert server_addresse[0]["address"] == "fce75e885241b4b465ad8e5919416ad4c9290d3e"
    assert (
        server_addresse[0]["private"]
        == "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d"
    )
