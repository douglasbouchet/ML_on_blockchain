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
    #basic_server = init_server()
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
    print(worker_pool[0].check_can_send_verification_parameters())
    for i, worker in enumerate(worker_pool):
        print("worker {} send encrypted model return {}".format(
            i, worker.send_encrypted_model()))
        print(worker_pool[0].check_can_send_verification_parameters())
        #print("worker {} send encrypted model return {}".format(i,worker.send_encrypted_model()))
    # make the workers send their verifications parameters
    # for worker in worker_pool:
    #    print(worker.check_can_send_verification_parameters())


if __name__ == "__main__":
    # basic_main()
    # hypervisor_based_main()
    # parallel_learning_main()
    # sequential_learning_main()
    encrypted_main()
