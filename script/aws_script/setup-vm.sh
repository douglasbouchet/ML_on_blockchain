#!/bin/sh
# Check that at least one IP address has been provided as an argument
if [ $# -lt 1 ]
then
    echo "Error: No IP addresses provided"
    echo "Call example: ./setup-vm.sh 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

# create the setup.yaml file for the given ip addresses
# ./create_setup.sh @

# check that the setup.yaml file has been created
if [ ! -f setup.yaml ]
then
    echo "Error: setup.yaml file not found"
    exit 1
fi

# generate the workload.yaml file
read -p "Generating workload, enter nb of workers: " n_workers
./create_workload.sh $n_workers

# check that workload.yaml exists
if [ ! -f workload.yaml ]
then
    echo "Error: workload.yaml file not found"
    exit 1
fi

timeout=5 # if the connection is not established within 5 seconds, exit with an error message

# copy smart contract folder to primary i.e should result in ubuntu@$1:contracts/learn_task. Also install required python packages to run arguments on primary
echo "copying smart contract folder to primary node + installing required python packages"
ssh ubuntu@$1 'mkdir -p contracts/learn_task && pip3 install coincurve && pip3 install pysha3'

if ! scp -o ConnectTimeout=$timeout ../../smart-contracts/federatedLearning/learn_task/arguments ubuntu@$1:~/contracts/learn_task; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$1 is reachable."
      exit 1
fi
if ! scp -o ConnectTimeout=$timeout ../../smart-contracts/federatedLearning/learn_task/contract.sol ubuntu@$1:~/contracts/learn_task; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$1 is reachable."
      exit 1
fi

for var in "$@";do # read the list of ip addresses

    # Use scp to copy the file to the remote IP address, and exit with an error message if nothing happens after 5 seconds
    if ! scp -o ConnectTimeout=$timeout workload.yaml ubuntu@$var:~; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$var is reachable."
      exit 1
    fi
    echo "sent workload.yaml to ubuntu@$var"
    if ! scp -o ConnectTimeout=$timeout setup.yaml ubuntu@$var:~; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: ubuntu@$var is reachable."
      exit 1
    fi
    echo "sent setup.yaml to ubuntu@$var"
done
