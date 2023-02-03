#!/bin/bash

# model size, 10k, 20k, 40k, 100k, 300k, 600k, 1M, 5M, 10M, 50M, 100M, 500M, 1B

# TODO update arguments to take the model length as argument, but but ok atm as we don't expect smart contract to work perfectly
# if constant time is true, no matter the model size, the verification time is the same (100s)
# if constant time is false, the verification time is proportional to the model size (base is 100s for 100k model size)

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ./vary_n_workers.sh <constant time (true/false)>"
    exit 1
fi

# model_lengths=( 50000 100000 300000 600000 1000000 10000000 )
model_lengths=( 50000 100000 300000 600000 1000000 5000000 10000000 )

for i in {1..1}; do # 3 measurements for each model length
    for model_length in "${model_lengths[@]}"; do
        # check if folder exists
        if [ ! -d "/home/user/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i" ]; then
            # create folder
            mkdir -p /home/user/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i
        fi
        num_workers=2
        for j in {1..9}; do
            echo "Testing blockchain with $num_workers workers, model length $model_length, run $i"
            # modify the solidity contract to test the model size
            ./create_smart_contract_bis.sh $model_length
            # create the workload for this model size and number of workers
            ./create_workload.sh $num_workers $model_length $1
            # TODO scp stuff in aws
            echo "Deploying blockchain..."
            # connect in ssh to launch the blockchain
            # timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
            timeout 35 ssh localhost "cd ~/minion && ./bin/minion run --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
            echo "Blockchain deployed"
            # open 2 ssh connections to launch primary and secondary
            echo "Launching primary and secondary"
            # ssh user@dclbigmem.epfl.ch -p 2232 'export PATH=/home/user/.local/bin:/home/user/anaconda3/bin:/home/user/anaconda3/condabin:/home/user/solidity/build/solc:/home/user/diablo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --stat --output=out.txt --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ 1 deploy/diablo/primary/setup.yaml ml_on_blockchain/workload/federated_learning.yaml; ' &
            # ssh localhost 'export PATH=/home/user/.local/bin:/home/user/anaconda3/bin:/home/user/anaconda3/condabin:/home/user/solidity/build/solc:/home/user/diablo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --stat --output=out.txt --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ 1 deploy/diablo/primary/setup.yaml ml_on_blockchain/workload/federated_learning.yaml; ' &
            ssh localhost 'export PATH=/home/user/.local/bin:/home/user/anaconda3/bin:/home/user/anaconda3/condabin:/home/user/solidity/build/solc:/home/user/diablo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary --stat --output=out.txt --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ 1 deploy/diablo/primary/setup.yaml ml_on_blockchain/workload/federated_learning.yaml; ' &
            # wait 5 seconds that primary is launched and then launch secondary
            sleep 5
            # ssh user@dclbigmem.epfl.ch -p 2232 "/home/user/diablo/diablo secondary -vvv localhost" &
            # ssh localhost "/home/user/diablo/diablo secondary -vvv localhost" &
            ssh localhost "/home/user/diablo/diablo secondary localhost" &
            wait
            echo "Done with primary and secondary"
            # scp user@dclbigmem.epfl.ch:out.txt ~/ml_on_blockchain/results/max_model_size/
            # copy the results from the primary to the local machine
            scp localhost:out.txt ~/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i/
            mv ~/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i/out.txt /home/user/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i/$num_workers.txt
            # touch /home/user/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i/$num_workers.txt
            # kill the blockchain: close all geth instances in parallel
            for ssh_port in {2233..2236}; do
                ssh user@dclbigmem.epfl.ch -p $ssh_port "pgrep geth | xargs kill -9" && echo "Closed geth instance on: $ssh_port" &
            done
            wait
            # wait 10 secondes
            echo "Waiting 10 seconds before restarting the blockchain"
            sleep 10
            num_workers=$((num_workers * 2))
        done
    done
done
echo "Done"
