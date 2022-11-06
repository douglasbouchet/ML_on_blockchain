import sys
import pytest

sys.path.append("/home/user/ml_on_blockchain")
from src.modules.federating_learning_server import FederatingLearningServer
from src.modules.hypervisor import Hypervisor


def test_job_finder_should_create_job_container_upon_creation():
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract("jobFinder", "JobFinder")
    assert job_finder_contract is not None
    # get_job should return current job container address
    models_weights, data_index = job_finder_contract.get_job()
    assert models_weights == 0
    assert data_index == 1


def test_submit_new_model():
    learning_server = FederatingLearningServer(3, 100, 10)
    hypervisor = Hypervisor()
    worker0 = hypervisor.create_mnist_worker()
    worker1 = hypervisor.create_mnist_worker()
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract("jobFinder", "JobFinder")
    hypervisor.set_contract(job_finder_contract)
    # get_job should return current job container address
    models_weights, data_index = job_finder_contract.get_job()
    # submit new model
    # job_finder_contract.submit_new_model(1, worker0.address, worker0.private_key)
    hypervisor.submit_new_model(1, worker0)
    # check that the model has been submitted
    received_models = job_finder_contract.get_received_models()
    assert len(received_models) == 1
