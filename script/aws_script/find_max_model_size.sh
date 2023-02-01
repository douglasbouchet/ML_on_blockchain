#!/bin/bash
# TODO maybe make each calculus 3/5 times and take the average
mkdir ~/ml_on_blockchain/results/max_model_size

# iterate from 1k to 50k
# for model_size in {1..50}; do
for model_size in {1..2}; do
    size=$((model_size * 1000))
    echo "Testing blockchain with $size model size"
    # modify the solidity contract to test the model size
    ./create_smart_contract_bis.sh $size
    # TODO scp stuff in aws
    echo "Deploying blockchain..."
    # connect in ssh to launch the blockchain
    # timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
    timeout 35 ssh localhost "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
    # open 2 ssh connections to launch primary and secondary
    echo "Launching primary and secondary"
    # ssh user@dclbigmem.epfl.ch -p 2232 'export PATH=/home/user/.local/bin:/home/user/anaconda3/bin:/home/user/anaconda3/condabin:/home/user/solidity/build/solc:/home/user/diablo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --stat --output=out.txt --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ 1 deploy/diablo/primary/setup.yaml ml_on_blockchain/workload/federated_learning.yaml; ' &
    ssh localhost 'export PATH=/home/user/.local/bin:/home/user/anaconda3/bin:/home/user/anaconda3/condabin:/home/user/solidity/build/solc:/home/user/diablo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --stat --output=out.txt --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ 1 deploy/diablo/primary/setup.yaml ml_on_blockchain/workload/federated_learning.yaml; ' &
    # wait 5 seconds that primary is launched and then launch secondary
    sleep 5
    # ssh user@dclbigmem.epfl.ch -p 2232 "/home/user/diablo/diablo secondary -vvv localhost" &
    ssh localhost "/home/user/diablo/diablo secondary -vvv localhost" &
    wait
    # copy the results from the primary to the local machine
    # scp user@dclbigmem.epfl.ch:out.txt ~/ml_on_blockchain/results/max_model_size/
    scp localhost:out.txt ~/ml_on_blockchain/results/max_model_size/
    mv ~/ml_on_blockchain/results/max_model_size/out.txt ~/ml_on_blockchain/results/max_model_size/$size.txt

    echo -e "\n"

    # kill the blockchain: close all geth instances in parallel
    for ssh_port in {2233..2236}; do
        ssh user@dclbigmem.epfl.ch -p $ssh_port "pgrep geth | xargs kill -9" && echo "Closed geth instance on: $ssh_port" &
    done
    wait
    echo -e "\n"
    # wait 10 secondes
    echo "Waiting 10 seconds before restarting the blockchain"
    sleep 10
done
