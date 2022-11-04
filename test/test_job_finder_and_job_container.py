import sys

sys.path.append("/home/user/ml_on_blockchain")
from src.modules.federating_learning_server import FederatingLearningServer


def test_job_finder_should_create_job_container_upon_creation():
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract("jobFinder", "JobFinder")
    assert job_finder_contract is not None
    # get_job should return current job container address
    models_weights, data_index = job_finder_contract.get_job()
    assert models_weights == 0
    assert data_index == 1
