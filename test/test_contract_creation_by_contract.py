import sys

sys.path.append("/home/user/ml_on_blockchain")
from src.modules.federating_learning_server import FederatingLearningServer


def test_hypervisor_based_main():
    # ------Init server and hypervisor--------
    # basic_server = init_server()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract("jobFinder", "JobFinder")
    assert job_finder_contract is not None
    assert job_finder_contract.get_job_container() is not None
    assert job_finder_contract.get_n_models_until_end() == 3
