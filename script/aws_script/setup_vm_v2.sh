#!/bin/sh
# Check that at least one IP address has been provided as an argument
if [ $# -lt 4 ]
then
    echo "Error: No IP addresses provided"
    echo "Call example: ./setup_vm_v2.sh <number of workers> <model_length> <constant time (true/false)> 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

n_workers=$1
model_length=$2
use_cste_time=$3
shift 3

all_nodes="$@"
primary="$1"
echo "all nodes:" $all_nodes
echo "primary:" $primary
shift


# create the setup.yaml file for the given ip addresses
./create_setup.sh "$@"

# check that the setup.yaml file has been created
if [ ! -f generated/setup.yaml ]
then
    echo "Error: generated/setup.yaml file not found"
    exit 1
fi

echo "Generating workload for:" $n_workers workers
./create_workload.sh $n_workers $model_length $use_cste_time

# check that workload.yaml exists
if [ ! -f generated/workload.yaml ]
then
    echo "Error: generated/workload.yaml file not found"
    exit 1
fi

echo "Generating smart contract with model length:" $model_length
./create_smartcontract.sh $n_workers $model_length

# check that smart contract  exists
if [ ! -f generated/contract.sol ]
then
    echo "Error: generated/contract.sol file not found"
    exit 1
fi

echo "Generating arguments for $n_workers"
./create_arguments.sh $n_workers $model_length

# check that smart contract  exists
if [ ! -f generated/arguments ]
then
    echo "Error: generated/arguments file not found"
    exit 1
fi

# give execution rights to generated/arguments
chmod u+x generated/arguments


timeout=5 # if the connection is not established within 5 seconds, exit with an error message

# copy smart contract folder to primary i.e should result in ubuntu@$1:contracts/learn_task. Also install required python packages to run arguments on primary
echo "copying smart contract folder to primary node + installing required python packages"
# ssh-keyscan -H primary >> ~/.ssh/known_hosts
# ssh ubuntu@$primary 'mkdir -p contracts/learn_task && pip3 install coincurve && pip3 install pysha3'
ssh -o "StrictHostKeyChecking no" ubuntu@$primary 'mkdir -p contracts/learn_task && pip3 install coincurve && pip3 install pysha3'

if ! scp -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout generated/arguments ubuntu@$primary:~/contracts/learn_task; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$primary is reachable."
      exit 1
fi
if ! scp -o StrictHostKeyChecking=no -o ConnectTimeout=$timeout generated/contract.sol ubuntu@$primary:~/contracts/learn_task; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$primary is reachable."
      exit 1
fi

for var in $all_nodes;do # read the list of ip addresses
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

echo "Setup complete."
