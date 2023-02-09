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

start_date=$(date)

size=33000
for model_size in {1..15}; do
    ./setup_vm_array_length.sh $size $primary_secondary_ip "$@"
    for run_nb in {11..20}; do # 10 measurements for each model length
        mkdir /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb
        echo "Testing array size for model size $size, run $run_nb"
        echo "Setup ended"
        echo "Deploying blockchain..."
        timeout 35 ssh localhost "( cd ~/aws/minion ; /home/user/aws/minion/bin/minion run -vv --breakpoint=chain quorum-ibft ../../workloads/counter.yaml $fleet_id )"
        echo "Blockchain deployed"
        echo "Launching primary"
        # give user execution rights to arguments
        ssh ubuntu@$primary_secondary_ip 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary -vvv --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 --stat 1 setup.yaml workload.yaml; ' &
        sleep 5
        echo "Launching secondary"
        ssh ubuntu@$primary_secondary_ip './install/diablo/diablo secondary -vvv --port=9000 --tag=any ' $primary_secondary_ip &
        wait
        echo "Benchmark ended"
        # # copy the results from the primary to the local machine
        scp ubuntu@$primary_secondary_ip:out.txt /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/
        mv /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/out.txt /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/$size.txt
        # touch /home/user/ml_on_blockchain/results/aws/varying_array_length/run_$run_nb/$size.txt
        # kill the blockchain: close all geth instances in parallel
        sleep 5
        echo "Stopping blockchain"
        ./stop_blockchain.sh "$@"
        echo "Waiting 10 seconds before restarting the blockchain"
        sleep 10
    done
    size=$(($size + 2000))
echo "Start date: " $start_date
echo "End date" $(date)
done

# sfr-d5c8b2a7-b516-4216-ae4c-e72887de3647@eu-west-3 13.37.211.217 13.39.50.170 15.188.53.211 35.180.118.73 52.47.141.1 15.188.8.68 13.39.16.238 13.38.93.38
