from src.modules.hypervisor import Hypervisor
from src.modules.federating_learning_server import FederatingLearningServer
import sys
import pytest
from web3.exceptions import ContractLogicError

sys.path.append("/home/user/ml_on_blockchain")


def test_job_finder_should_create_job_container_upon_creation():
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract(
        "jobFinder", "JobFinder")
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
    worker2 = hypervisor.create_mnist_worker()
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract(
        "jobFinder", "JobFinder")
    hypervisor.set_contract(job_finder_contract)
    # get_job should return current job container address
    models_weights, data_index = job_finder_contract.get_job()
    # there should be no previous jobs addresses yet
    all_prev_job_best_model = job_finder_contract.get_all_previous_jobs_best_model()
    assert len(all_prev_job_best_model) == 0
    # submit new model
    hypervisor.submit_new_model(1, worker0)
    hypervisor.submit_new_model(1, worker1)
    received_models = job_finder_contract.get_received_models()
    assert len(received_models) == 2
    # worker submitting twice for the same job should throw exception
    with pytest.raises(ContractLogicError):
        hypervisor.submit_new_model(1, worker0)
    with pytest.raises(ContractLogicError):
        hypervisor.submit_new_model(3, worker1)
    received_models = job_finder_contract.get_received_models()
    assert len(received_models) == 2
    # we need 3 different models to finish the job
    hypervisor.submit_new_model(1, worker2)
    # now the smart contract should have elected a model as the best one
    all_prev_job_best_model = job_finder_contract.get_all_previous_jobs_best_model()
    assert len(all_prev_job_best_model) == 1
    # all workers send the same model of 1
    assert all_prev_job_best_model[0] == 1
    # TODO check that the best model is the one with the highest number of votes
    # we should be able to get the new job
    assert job_finder_contract.get_job() == [
        1,
        2,
    ]  # model weight is 1 and data index is 2 (only valid until learning server don't really put updated model)
    # the new job shouldn't have any received models yet
    received_models = job_finder_contract.get_received_models()
    assert len(received_models) == 0
    # submit new model
    hypervisor.submit_new_model(3, worker0)
    hypervisor.submit_new_model(2, worker1)
    received_models = job_finder_contract.get_received_models()
    assert len(received_models) == 2
    hypervisor.submit_new_model(2, worker2)
    # now the smart contract should have elected a model as the best one
    all_prev_job_best_model = job_finder_contract.get_all_previous_jobs_best_model()
    assert len(all_prev_job_best_model) == 2
    # TODO check that the best model is the one with the highest number of votes
    assert all_prev_job_best_model[0] == 1
    assert all_prev_job_best_model[1] == 2  # majority of weights is 2


def test_paying_of_workers():
    learning_server = FederatingLearningServer(3, 100, 10)
    hypervisor = Hypervisor()
    worker0 = hypervisor.create_mnist_worker()
    worker1 = hypervisor.create_mnist_worker()
    worker2 = hypervisor.create_mnist_worker()
    # ------Deploy smart contract---------
    job_finder_contract = learning_server.deploy_contract(
        "jobFinder", "JobFinder")
    hypervisor.set_contract(job_finder_contract)
    # ------Make workers submit models-------
    hypervisor.submit_new_model(1, worker0)
    hypervisor.submit_new_model(1, worker1)
    hypervisor.submit_new_model(2, worker2)
    # ----- Check that workers got paid -------
    assert worker0.get_balance() == 0
    assert worker1.get_balance() == 0
    assert worker2.get_balance() == 0
