from src.basic_server import BasicServer
from src.basic_worker import BasicWorker
from src.modules.hypervisor import Hypervisor
from src.modules.parallelized_hypervisor import ParallelizedHypervisor
from src.modules.encrypted_hypervisor import EncryptedHypervisor
from src.modules.federating_learning_server import FederatingLearningServer


def init_server():
    server_address = "fce75e885241b4b465ad8e5919416ad4c9290d3e"
    server_private_key = (
        "bde4a6df57a58a186ed2099754877a16bd48a10bc4469377d9840f475772723d"
    )
    basic_server = BasicServer(server_address, server_private_key)
    return basic_server


def create_single_worker():
    worker_address = "ad8c4637330e8eab5eadbbda59910a9d926274b2"
    worker_private_key = (
        "9793a9cb6042ef94219797af47062b38100e535fdb7034a2ae9ba4136a6d17b4"
    )
    basic_worker = BasicWorker(worker_address, worker_private_key)
    return basic_worker


def basic_main():
    # ------Init server and worker--------
    # basic_server = init_server()
    learning_server = FederatingLearningServer(3, 100, 10)
    basic_worker = create_single_worker()
    # ------Deploy smart contract---------
    # contract = basic_server.deploy("incrementer")
    # contract = basic_server.deploy("register", "Register")
    # contract = learning_server.deploy_contract("register", "Register")
    # contract = learning_server.deploy_contract("fragmentedJobFinder", "FragmentedJobFinder")
    contract = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder")
    # print("Initial number of workers:", contract.get_number_of_workers())
    # ------Register worker to server-----
    # basic_worker.register_to_learning(contract.contract_address, contract.abi)
    # print("current number of workers:", contract.get_number_of_workers())


def hypervisor_based_main():
    # ------Init server and hypervisor--------
    basic_server = init_server()
    hypervisor = Hypervisor()
    # ------Deploy smart contract---------
    contract = basic_server.deploy("register", "Register")
    print("Initial number of workers:", contract.get_number_of_workers())
    # ------Give contract information to hypervisor-----
    hypervisor.set_contract(contract)
    # ------Create some workers-----------
    worker0 = hypervisor.create_worker()
    worker1 = hypervisor.create_worker()
    # ------Register worker to server-----
    hypervisor.make_worker_join_learning(worker0)
    hypervisor.make_worker_join_learning(worker1)
    print("current number of workers:", contract.get_number_of_workers())
    # ------Unregister worker from server-----
    hypervisor.make_worker_leave_learning(worker0)
    print("current number of workers:", contract.get_number_of_workers())
    hypervisor.make_worker_leave_learning(worker1)
    print("current number of workers:", contract.get_number_of_workers())
    hypervisor.make_worker_leave_learning(worker0)
    assert contract.get_number_of_workers() == 0


def parallel_learning_main():
    # ------Init server and hypervisor--------
    parallel_hypervisor = ParallelizedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    fragmented_job_finder = learning_server.deploy_contract(
        "fragmentedJobFinder", "FragmentedJobFinder"
    )
    parallel_hypervisor.contract = fragmented_job_finder
    # init the workers
    parallel_hypervisor.create_wait_workers(number_of_workers=999)
    # worker_pool = parallel_hypervisor.select_worker_pool(pool_size=10)
    # worker_pool = parallel_hypervisor.select_worker_pool(pool_size=3)
    worker_pool = parallel_hypervisor.select_worker_pool(pool_size=2)
    print("Number of workers in the pool:", len(worker_pool))
    get_processes = parallel_hypervisor.create_get_weights_process(worker_pool)
    print("Number of processes:", len(get_processes))

    parallel_hypervisor.perform_one_process_step(get_processes)
    print("get parameters finished")
    fake_learn_processess = parallel_hypervisor.create_fake_learn_process(
        worker_pool)
    parallel_hypervisor.perform_one_process_step(fake_learn_processess)
    print("learn finished")
    send_processes = parallel_hypervisor.create_send_weights_process(
        worker_pool)
    parallel_hypervisor.perform_one_process_step(send_processes)
    print("send parameters finished")


def sequential_learning_main():
    # ------Init server and hypervisor--------
    parallel_hypervisor = ParallelizedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    fragmented_job_finder = learning_server.deploy_contract(
        "fragmentedJobFinder", "FragmentedJobFinder"
    )
    parallel_hypervisor.contract = fragmented_job_finder
    # init the workers
    parallel_hypervisor.create_wait_workers(number_of_workers=999)
    worker_pool = parallel_hypervisor.select_worker_pool(pool_size=2)
    print("sequential execution but random order")
    parallel_hypervisor.perform_get_weights(worker_pool)
    print("parallel execution (no interaction with smart contract)")
    parallel_hypervisor.perform_parallel_fake_learn(worker_pool)
    print("sequential execution but random order")
    parallel_hypervisor.perform_send_fragment(worker_pool)


def encrypted_main():
    encrypted_hypervisor = EncryptedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    encrypted_job_finder = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder"
    )
    encrypted_hypervisor.contract = encrypted_job_finder
    # init the workers
    encrypted_hypervisor.create_encrypted_workers(number_of_workers=999)
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=5)
    # make the workers join the learning
    # TODO
    # make the workers send their learned models
    # print(worker_pool[0].check_can_send_verification_parameters())
    good_model = 97
    wrong_model = 98

    for i, worker in enumerate(worker_pool[:3]):
        print("worker {} send encrypted model return {}".format(
            i, worker.send_encrypted_model(good_model)))
        print(worker_pool[0].check_can_send_verification_parameters())
        if i == 0:
            #  this should throw an error as not enough models were sent
            print("Worker 0 send veritication parameters return:",
                  worker_pool[0].send_verifications(good_model=True))
    # make the workers send their verifications parameters
    for i, worker in enumerate(worker_pool):
        print("worker {} send verification parameters ".format(i))
        print("model is ready:{}".format(
            encrypted_job_finder.get_model_is_ready()))
        worker.send_verifications(good_model=True)
    # after all workers send their verifications, the server should have decrypted the model
    print("model is ready:{}".format(encrypted_job_finder.get_model_is_ready()))


def simple_encryption_check():
    encrypted_hypervisor = EncryptedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    encrypted_job_finder = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder"
    )
    encrypted_hypervisor.contract = encrypted_job_finder
    # init the workers
    encrypted_hypervisor.create_encrypted_workers(number_of_workers=999)
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=5)
    good_model = 97
    wrong_model = 98
    worker_pool[0].compare_hash()  # should return true
    # make workers 1 to 3 sends their models
    for i, worker in enumerate(worker_pool[:3]):
        res = worker.send_encrypted_model(good_model)
        assert res is True
        print("Worker {} sending model: ".format(i), res)
        # send again a model should return false as model is rejected
        # assert worker.send_encrypted_model() == False

    # we check if we can send the verification parameters
    print("can send:", worker_pool[0].check_can_send_verification_parameters())
    # now job has received enough models, it shoudn't accept any more models
    for i, worker in enumerate(worker_pool[3:]):
        res = worker.send_encrypted_model(wrong_model)
        assert res is False
        print("Worker {} sending model: ".format(i), res)

    # we check that we can send the verification parameters only for worker who did send a model
    for i, worker in enumerate(worker_pool[:3]):
        res = worker.check_can_send_verification_parameters()
        # print("Worker {} check_can_send_verification_parameters: ".format(i), res)
        assert res is True
    for i, worker in enumerate(worker_pool[3:]):
        res = worker.check_can_send_verification_parameters()
        # print("Worker {} check_can_send_verification_parameters: ".format(i), res)
        assert res is False

    # now we send the verification parameters
    for i, worker in enumerate(worker_pool[:2]):
        res = worker.send_verifications(good_model=True, good_address=True)
        print("Worker {} sending verification parameters: ".format(i), res)
        assert res is True
        print("model is ready:{}".format(
            encrypted_job_finder.get_model_is_ready()))

    # we send a model different that the first one we send, so should be rejected
    res = worker_pool[2].send_verifications(
        good_model=False, good_address=True)
    print("Worker {} sending verification parameters with wrong model but good address: ".format(2), res)
    assert res is False
    res = worker_pool[2].send_verifications(
        good_model=True, good_address=False)
    print("Worker {} sending verification parameters with good model but wrong address: ".format(2), res)
    assert res is False
    res = worker_pool[2].send_verifications(good_model=True, good_address=True)
    print("Worker {} sending verification parameters with good model and address but enough model received so still\
         deny: ".format(2), res)
    assert res is False

    for i, worker in enumerate(worker_pool[3:]):
        res = worker.send_verifications(good_model=True, good_address=True)
        print("Worker {} sending verification parameters: ".format(i), res)
        assert res is False

    # we check if the model is ready
    res = encrypted_job_finder.get_model_is_ready()
    print("model is ready:{}".format(res))
    assert res is True
    # we check value of the model
    res = encrypted_job_finder.get_final_model()
    print("model value:{}".format(res))
    assert res[0] == 97 and res[1] is True


def simple_learning_scenario():
    """
    In this scenario we have 6 workers, 3 of them send the same model (97), 2 send a different model (98)
    and one send a model (99). Best model should be the one with value 97
    """
    encrypted_hypervisor = EncryptedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    encrypted_job_finder = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder"
    )
    encrypted_hypervisor.contract = encrypted_job_finder
    # init the workers
    encrypted_hypervisor.create_encrypted_workers(number_of_workers=999)
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=6)
    for i, worker in enumerate(worker_pool):
        if i < 3:
            assert worker.send_encrypted_model(model=97) is True
        elif i < 5:
            assert worker.send_encrypted_model(model=98) is True
        else:
            assert worker.send_encrypted_model(model=99) is True

    assert worker_pool[0].check_can_send_verification_parameters() is True

    # now we send the verification parameters (all workers send the same model they learned with correct address)
    # we send weights in following order: 97, 97, 98, 99, 98, 97 so we reach the threshold of 3 at the end
    for i in [0, 1, 3, 5, 4, 2]:
        assert worker_pool[i].send_verifications(
            good_model=True, good_address=True) is True
        # we check if the model is ready
        print("{} model is ready:{}".format(i,
                                            encrypted_job_finder.get_model_is_ready()))

    # we check if the model is ready
    res = encrypted_job_finder.get_model_is_ready()
    print("model is ready:{}".format(res))
    assert res is True
    # we check value of the model
    res = encrypted_job_finder.get_final_model()
    print("model value:{}".format(res))
    assert res[0] == 97 and res[1] is True


def multiple_learn_tasks_scenario():
    """
    In this scenario we have 6 workers, 3 of them send the same model (97), 2 send a different model (98)
    and one send a model (99). Best model should be the one with value 97
    This is for the first learning task, then we do another learning task with 3 workers sending 98, 2 sending 97
     and 1 sending 99. Best model should be 98
    Finally we do a third learning task with 3 workers sending 99, 2 sending 98 and 1 sending 97.
     Best model should be 99
    Also some we select a different worker pool for each learning task (and keep old workers in the pool)
    """
    encrypted_hypervisor = EncryptedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    encrypted_job_finder = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder"
    )
    encrypted_hypervisor.contract = encrypted_job_finder
    # init the workers
    encrypted_hypervisor.create_encrypted_workers(number_of_workers=999)
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=6)
    for i, worker in enumerate(worker_pool):
        if i < 3:
            assert worker.send_encrypted_model(model=97) is True
        elif i < 5:
            assert worker.send_encrypted_model(model=98) is True
        else:
            assert worker.send_encrypted_model(model=99) is True

    assert worker_pool[0].check_can_send_verification_parameters() is True

    # now we send the verification parameters (all workers send the same model they learned with correct address)
    # we send weights in following order: 97, 97, 98, 99, 98, 97 so we reach the threshold of 3 at the end
    for i in [0, 1, 3, 5, 4, 2]:
        assert worker_pool[i].send_verifications(
            good_model=True, good_address=True) is True
        # we check if the model is ready
        print("{} model is ready:{}".format(i,
                                            encrypted_job_finder.get_model_is_ready()))

    # we check if the model is ready
    res = encrypted_job_finder.get_model_is_ready()
    print("model is ready:{}".format(res))
    assert res is True
    # we check value of the model
    res = encrypted_job_finder.get_final_model()
    print("model value:{}".format(res))
    assert res[0] == 97 and res[1] is True

    # now we do another learning task with 3 workers sending 98, 2 sending 97 and 1 sending 99. Best model should be 98
    # keep 2 worker from previous pool
    # we select a different worker pool for this learning task
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=9)[-6:]

    for i, worker in enumerate(worker_pool):
        if i < 3:
            assert worker.send_encrypted_model(model=98) is True
        elif i < 5:
            assert worker.send_encrypted_model(model=99) is True
        else:
            assert worker.send_encrypted_model(model=100) is True

    assert worker_pool[0].check_can_send_verification_parameters() is True

    # now we send the verification parameters (all workers send the same model they learned with correct address)
    for i in [0, 1, 3, 5, 4, 2]:
        assert worker_pool[i].send_verifications(
            good_model=True, good_address=True) is True
        # we check if the model is ready
        print("{} model is ready:{}".format(i,
                                            encrypted_job_finder.get_model_is_ready()))

    # we check if the model is ready
    res = encrypted_job_finder.get_model_is_ready()
    print("model is ready:{}".format(res))
    assert res is True
    # we check value of the model
    res = encrypted_job_finder.get_final_model()
    print("model value:{}".format(res))
    assert res[0] == 98 and res[1] is True


def variable_model_complexity():
    """In this scenario we test the functionality of the contract when the model complexity is not constant
    This correspond to sending different number of weights to the contract
    Use thresholdForBestModel = 2;
    thresholdMaxNumberReceivedModels = 3;
    """
    encrypted_hypervisor = EncryptedHypervisor()
    learning_server = FederatingLearningServer(3, 100, 10)
    # ------Deploy smart contract---------
    encrypted_job_finder = learning_server.deploy_contract(
        "encryptionJobFinder", "EncryptionJobFinder"
    )
    encrypted_hypervisor.contract = encrypted_job_finder
    # init the workers
    encrypted_hypervisor.create_encrypted_workers(number_of_workers=999)
    worker_pool = encrypted_hypervisor.select_worker_pool(pool_size=5)
    good_model = 97
    wrong_model = 98
    worker_pool[0].compare_hash()  # should return true
    # make workers 1 to 3 sends their models
    for i, worker in enumerate(worker_pool[:3]):
        res = worker.send_encrypted_model(good_model)
        assert res is True
        print("Worker {} sending model: ".format(i), res)
        # send again a model should return false as model is rejected
        # assert worker.send_encrypted_model() == False

    # we check if we can send the verification parameters
    print("can send:", worker_pool[0].check_can_send_verification_parameters())
    # now job has received enough models, it shoudn't accept any more models
    for i, worker in enumerate(worker_pool[3:]):
        res = worker.send_encrypted_model(wrong_model)
        assert res is False
        print("Worker {} sending model: ".format(i), res)

    # we check that we can send the verification parameters only for worker who did send a model
    for i, worker in enumerate(worker_pool[:3]):
        res = worker.check_can_send_verification_parameters()
        # print("Worker {} check_can_send_verification_parameters: ".format(i), res)
        assert res is True
    for i, worker in enumerate(worker_pool[3:]):
        res = worker.check_can_send_verification_parameters()
        # print("Worker {} check_can_send_verification_parameters: ".format(i), res)
        assert res is False

    # now we send the verification parameters
    for i, worker in enumerate(worker_pool[:2]):
        res = worker.send_verifications(good_model=True, good_address=True)
        print("Worker {} sending verification parameters: ".format(i), res)
        assert res is True
        print("model is ready:{}".format(
            encrypted_job_finder.get_model_is_ready()))

    # we send a model different that the first one we send, so should be rejected
    res = worker_pool[2].send_verifications(
        good_model=False, good_address=True)
    print("Worker {} sending verification parameters with wrong model but good address: ".format(2), res)
    assert res is False
    res = worker_pool[2].send_verifications(
        good_model=True, good_address=False)
    print("Worker {} sending verification parameters with good model but wrong address: ".format(2), res)
    assert res is False
    res = worker_pool[2].send_verifications(good_model=True, good_address=True)
    print("Worker {} sending verification parameters with good model and address but enough model received so still\
         deny: ".format(2), res)
    assert res is False

    for i, worker in enumerate(worker_pool[3:]):
        res = worker.send_verifications(good_model=True, good_address=True)
        print("Worker {} sending verification parameters: ".format(i), res)
        assert res is False

    # we check if the model is ready
    res = encrypted_job_finder.get_model_is_ready()
    print("model is ready:{}".format(res))
    assert res is True
    # we check value of the model
    res = encrypted_job_finder.get_final_model()
    print("model value:{}".format(res))
    assert res[0][0] == 97 and res[1] is True


if __name__ == "__main__":
    # basic_main()
    # hypervisor_based_main()
    # parallel_learning_main()
    # sequential_learning_main()
    # encrypted_main()
    # simple_encryption_check()
    # simple_learning_scenario()
    # multiple_learn_tasks_scenario()
    variable_model_complexity()
