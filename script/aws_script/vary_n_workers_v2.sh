#!/bin/bash

# first ip address is primary address
# TODO check that primary and secondary addresses are equals, otw don't work
if [ $# -lt 2 ]; then
    echo "Error: Need provide at least 2 IP addresses"
    echo "Usage: $0  <constant time (true/false)> <fleet_id-id> 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

constant_time=$1
echo "constant_time:" $constant_time
shift 1
fleet_id=$1
echo "fleet_id:" $fleet_id
shift 1
primary_secondary_ip=$1
echo "primary_secondary_ip:" $primary_secondary_ip
shift 1
echo "remaining arguments: $@"

if [ $constant_time = "true" ]; then
    folder="constant_time"
else
    folder="varying_time"
fi

echo "folder:" $folder


# model_lengths=( 50000 100000 300000 600000 1000000 5000000)
# model_lengths=( 50000 100000 300000 600000 1000000 )
# model_lengths=( 50000 100000 300000 600000 )
model_lengths=( 200000 )
# model_lengths=( 5000000 )

# TODO this point the blockchain should already have been deployed and cut

for i in {1..1}; do # 2 measurements for each model length
    for model_length in "${model_lengths[@]}"; do
        # check if folder exists
        if [ ! -d "/home/user/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i" ]; then
            # create folder
            mkdir -p /home/user/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i
        fi
        num_workers=1
        # for j in {1..9}; do
        for j in {1..7}; do
        # for j in {1..1}; do
            echo "Testing blockchain with $num_workers workers, model length $model_length, run $i"
            echo "setting up nodes"
            ./setup_vm_v2.sh $num_workers $model_length $constant_time $primary_secondary_ip "$@"
            echo "Setup ended"
            echo "Deploying blockchain..."
            timeout 40 ssh localhost "( cd ~/aws/minion ; /home/user/aws/minion/bin/minion run -vv --breakpoint=chain quorum-ibft ../../workloads/counter.yaml $fleet_id )"
            echo "Blockchain deployed"
            # open 2 ssh connections to launch primary and secondary
            echo "Launching primary"
            # give user execution rights to arguments
            # ssh ubuntu@$primary_secondary_ip './install/diablo/diablo primary -vvv --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 --stat 1 setup.yaml workload.yaml; ' &
            ssh ubuntu@$primary_secondary_ip 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary -vvv --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 --stat 1 setup.yaml workload.yaml; ' &
            #ssh ubuntu@$primary_secondary_ip 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 --stat 1 setup.yaml workload.yaml; ' &
            sleep 5
            echo "Launching secondary"
            ssh ubuntu@$primary_secondary_ip './install/diablo/diablo secondary -vvv --port=9000 --tag=any ' $primary_secondary_ip &
            #ssh ubuntu@$primary_secondary_ip './install/diablo/diablo secondary --port=9000 --tag=any ' $primary_secondary_ip &
            wait
            echo "Benchmark ended"
            # # copy the results from the primary to the local machine
            scp ubuntu@$primary_secondary_ip:out.txt ~/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i/
            mv ~/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i/out.txt /home/user/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i/$num_workers.txt
            # # touch /home/user/ml_on_blockchain/results/aws/varying_workers/$folder/model_length_$model_length/run_$i/$num_workers.txt
            # # kill the blockchain: close all geth instances in parallel
            sleep 5
            echo "Stopping blockchain"
            ./stop_blockchain.sh "$@"
            echo "Waiting 10 seconds before restarting the blockchain"
            sleep 10
            num_workers=$((num_workers * 2))
        done
    done
done
# print current time to know when the script ended
date
echo "Done"

# sfr-8d1341e7-facf-4c81-b122-68cc96c44d05@eu-west-3 35.180.243.182 52.47.121.193 13.37.213.34 13.38.245.132 15.236.207.167 35.180.42.100 15.188.54.19 52.47.190.21
