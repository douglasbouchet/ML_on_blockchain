#!/bin/bash
# TODO maybe make each calculus 3/5 times and take the average



#!/bin/bash

# first ip address is primary address
# TODO check that primary and secondary addresses are equals, otw don't work
if [ $# -lt 3 ]; then
    echo "Error: Need provide at least 2 IP addresses"
    echo "Usage: $0 <fleet id> <primary and secondary ip> <node ip 0> <node ip 1> ..."
    exit 1
fi


fleet_id=$1
primary_secondary_ip=$2
echo "primary_secondary_ip:" $primary_secondary_ip
shift 2
echo "remaining arguments: $@"


for run_nb in {1..9}; do # 6 measurements for each model length
    mkdir /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb
    for model_size in {1..50}; do
        size=$(($model_size * 1000))
        echo "Testing array size for model size $size, run $run_nb"
        # ./setup_vm_array_length $model_length $primary_secondary_ip "$@"
        # echo "Setup ended"
        # echo "Deploying blockchain..."
        # timeout 40 ssh localhost "( cd ~/aws/minion ; /home/user/aws/minion/bin/minion run -vv --breakpoint=chain quorum-ibft ../../workloads/counter.yaml $fleet_id )"
        # echo "Blockchain deployed"
        # echo "Launching primary"
        # # give user execution rights to arguments
        # ssh ubuntu@$primary_secondary_ip 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary -vvv --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 --stat 1 setup.yaml workload.yaml; ' &
        # sleep 5
        # echo "Launching secondary"
        # ssh ubuntu@$primary_secondary_ip './install/diablo/diablo secondary -vvv --port=9000 --tag=any ' $primary_secondary_ip &
        # wait
        # echo "Benchmark ended"
        # # # copy the results from the primary to the local machine
        # scp ubuntu@$primary_secondary_ip:out.txt /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/
        # scp ubuntu@$primary_secondary_ip:out.txt ~/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i/
        # mv /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/out.txt /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/$size.txt
        touch /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/$size.txt
        # # kill the blockchain: close all geth instances in parallel
        # sleep 5
        # echo "Stopping blockchain"
        # ./stop_blockchain.sh "$@"
        # echo "Waiting 10 seconds before restarting the blockchain"
        # sleep 10
    done
done
date
echo "Done"
