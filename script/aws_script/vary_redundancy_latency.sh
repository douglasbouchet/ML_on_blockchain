#!/bin/bash

function copy_file_to_vm {

    primary=$1
    shift 1
    timeout=5 # if the connection is not established within 5 seconds, exit with an error message
    # copy smart contract folder to primary i.e should result in ubuntu@$1:contracts/learn_task. Also install required python packages to run arguments on primary
    echo "copying smart contract folder to primary node + installing required python packages"
    ssh -o "StrictHostKeyChecking no" ubuntu@$primary 'mkdir -p contracts/learn_task && pip3 install coincurve && pip3 install pysha3'

    if ! scp -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout generated/arguments ubuntu@$primary:~/contracts/learn_task; then
          echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$primary is reachable."
          exit 1
    fi
    if ! scp -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout generated/contract.sol ubuntu@$primary:~/contracts/learn_task; then
          echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$primary is reachable."
          exit 1
    fi

    for var in $@;do # read the list of ip addresses
        # echo "copying files to node: $var"
        # Use scp to copy the file to the remote IP address, and exit with an error message if nothing happens after 5 seconds
        if ! scp -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout generated/workload.yaml ubuntu@$var:~; then
          echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$var is reachable."
          exit 1
        fi
        if ! scp -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout generated/setup.yaml ubuntu@$var:~; then
          echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$var is reachable."
          exit 1
        fi
    done
}

# first ip address is primary address
if [ $# -lt 2 ]; then
    echo "Error: Need provide at least 2 IP addresses"
    echo "Usage: $0  <fleet_id-id> 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

fleet_id=$1
echo "fleet_id:" $fleet_id
shift 1
primary_secondary_ip=$1
echo "primary_secondary_ip:" $primary_secondary_ip
shift 1
echo "remaining arguments: $@"


model_length=1000000
redundancies=( 1 2 4 8 16 32 )
paces=( 0.05 0.1 0.25 0.5 1 )

# make sure we are using the correct contract

./create_setup.sh "$@"

# iterate over all the redundancy values
for redundancy in "${redundancies[@]}"; do
    # iterate over all the paces
    # create a folder for the current redundancy
    folder=redundancy_$redundancy
    if [ ! -d "/home/user/ml_on_blockchain/results/aws/redundancy_pace/$folder" ]; then
        # create folder
        mkdir -p /home/user/ml_on_blockchain/results/aws/redundancy_pace/$folder
    fi
    # create arguments for the current redundancy
    echo "Generating arguments for $n_workers"
    ./create_arguments.sh $redundancy $model_length
    for pace in "${paces[@]}"; do
        echo "Testing redundancy $redundancy, pace $pace"
        # create the workload for this experiment
        ./create_workload_red_pace.sh $redundancy $model_length $pace
        # then we can copy the files to the vms
        copy_file_to_vm $primary_secondary_ip "$@"
        file=pace_$pace.txt
        # touch /home/user/ml_on_blockchain/results/aws/redundancy_pace/$folder/$file
        echo "Deploying blockchain..."
        timeout 40 ssh localhost "( cd ~/aws/minion ; /home/user/aws/minion/bin/minion run -vv --breakpoint=chain quorum-ibft ../../workloads/counter.yaml $fleet_id )"
        echo "Launching primary"
        ssh ubuntu@$primary_secondary_ip 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary -vvv --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 --stat 1 setup.yaml workload.yaml; ' &
        sleep 5
        echo "Launching secondary"
        ssh ubuntu@$primary_secondary_ip './install/diablo/diablo secondary -vvv --port=9000 --tag=any ' $primary_secondary_ip &
        wait
        echo "$redundancy, $pace finsihed"
        # # copy the results from the primary to the local machine
        scp ubuntu@$primary_secondary_ip:out.txt /home/user/ml_on_blockchain/results/aws/redundancy_pace/$folder/out.txt
        mv /home/user/ml_on_blockchain/results/aws/redundancy_pace/$folder/out.txt /home/user/ml_on_blockchain/results/aws/redundancy_pace/$folder/$file
        # # kill the blockchain: close all geth instances in parallel
        sleep 5
        echo "Stopping blockchain"
        ./stop_blockchain.sh "$@"
        echo "Waiting 10 seconds before restarting the blockchain"
        sleep 10
    done
done
echo "End of experiment"
