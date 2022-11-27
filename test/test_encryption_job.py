import pytest
from src.modules.parallelized_hypervisor import ParallelizedHypervisor
from src.modules.encrypted_hypervisor import EncryptedHypervisor
from src.modules.federating_learning_server import FederatingLearningServer


def test_stupid():
    # This is a stupid test, but it's a start.
    print("hello world")
    assert True


def test_encryption_worker():
    encrypted_hypervisor = EncryptedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    encrypted_job_finder = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder"
    )
    # check that contract 'encryptionJobFinder' was deployed
    assert encrypted_job_finder is not None
    encrypted_hypervisor.contract = encrypted_job_finder
    encrypted_hypervisor.create_encrypted_workers(number_of_workers=999)
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=5)
    assert len(worker_pool) == 5  # check that 5 workers were selected
    assert worker_pool[0].check_can_send_verification_parameters() == False
    model_value, model_ready = encrypted_job_finder.get_final_model()
    assert model_ready == False
    assert model_value == b'0x0\x00'
    # TEST of send_encrypted_model
    for i, worker in enumerate(worker_pool[:3]):
        assert worker.send_encrypted_model() == True  #  check model was correctly sent
        #  check that the worker can't send the model twice
        assert worker.send_encrypted_model() == False
        if i < 2:
            for worker_bis in worker_pool:
                assert worker_bis.check_can_send_verification_parameters() == False
                assert worker_bis.send_verifications() == False
        # now that we sent 3 models, we should be able to send verification parameters
        else:
            for worker_bis in worker_pool:
                assert worker_bis.check_can_send_verification_parameters() == True
                # but only worker 0,1,2 should be able to send verifications as other ones
                # didn't send their model
                if worker_bis.id in [0, 1, 2]:
                    assert worker_bis.send_verifications() == True
                else:
                    assert worker_bis.send_verifications() == False
    # Now that the learning phase is over, we should be able to see the final model
    assert encrypted_job_finder.get_model_is_ready() == True
    model_value, model_ready = encrypted_job_finder.get_final_model()
    assert model_ready == True
    print("model_value:", model_value)
    # assert model_value != "0x0"
