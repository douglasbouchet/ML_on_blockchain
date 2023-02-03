#!/bin/bash

# expect a list of ip addresses as arguments. First one is primary address and the rest are secondary addresses
if [ $# -lt 2 ]
then
    echo "Error: Need provide at least 2 IP addresses"
    exit 1
fi


# setup file for results
file_name="$num_workers"_workers_"$redundancy"_redundancy_"$model_length"_model_length
# if res/$scenario does not exist, create it
if [ ! -d res/$scenario ]; then
    mkdir res/$scenario
fi
touch res/$scenario/$file_name.txt

# count the number of arguments
num_args=$#
# subtract 1 to get the number of secondary addresses
num_secondary=$((num_args - 1))
echo "Number of secondary addresses: $num_secondary"

# connect to primary and launch diablo primary
ssh ubuntu@$1 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 -vvv --stat '"$num_secondary"' setup.yaml workload.yaml; ' &
# wait 5 seconds that primary is launched and then launch secondary
sleep 5
# connect to each secondary and launch diablo secondary
for var in "${@:2}";do
    # ssh ubuntu@$var './install/diablo/diablo secondary -vvv --port=3000 --tag=any ' $1 &
    ssh ubuntu@$var './install/diablo/diablo secondary -vvv --port=9000 --tag=any ' $1 &
done
wait
# copy the result file from primary to local machine
scp ubuntu@$1:out.txt res/
mv res/out.txt res/$scenario/$file_name.txt
echo -e "\n"

# end machine: see if sufficient to just kill all geth processes
# TODO

# expect a list of ip addresses as arguments. First one is primary address and the rest are secondary addresses
if [ $# -lt 2 ]
then
    echo "Error: Need provide at least 2 IP addresses"
    exit 1
fi

# n workers x
# red x
# models x
# constant time yes
# nodes ids yes

# first ip address is primary address
# TODO check that primary and secondary addresses are equals, otw don't work
if [ $# -lt 2 ]
then
    echo "Error: Need provide at least 2 IP addresses"
    echo "Usage: ./vary_n_workers_v2  <constant time (true/false)> <fleet_id-id> 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

constant_time=$1
echo "constant_time:" $constant_time
shift 1
fleet_id=$1
echo "fleet_id-id:" $fleet_id
shift 1
primary_secondary_ip=$1
echo "primary_secondary_ip:" $primary_secondary_ip
shift 1
echo "remaining arguments: $@"

# model_lengths=( 50000 100000 1000000 )
model_lengths=( 100000 1000000 )

# TODO this point the blockchain should already have been deployed and cut

for i in {1..2}; do # 3 measurements for each model length
    for model_length in "${model_lengths[@]}"; do
        # check if folder exists
        if [ ! -d "/home/user/ml_on_blockchain/results/aws/varying_workers/constant_time/model_length_$model_length/run_$i" ]; then
            # create folder
            mkdir -p /home/user/ml_on_blockchain/results/aws/varying_workers/constant_time/model_length_$model_length/run_$i
        fi
        num_workers=1
        for j in {1..2}; do
            echo "Testing blockchain with $num_workers workers, model length $model_length, run $i"
            echo "setting up nodes"
            # /setup-vm_v2.sh <number of workers> <model_length> <constant time (true/false)> 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
            ./setup_vm_v2.sh $num_workers $model_length $constant_time $primary_secondary_ip "$@"
            echo "Nodes setup"
            # create the workload for this model size and number of workers
            # ./create_workload.sh $num_workers $model_length $1
            # ssh ubuntu@$1 './bin/minion run -vv --breakpoint=chain quorum-ibft ../../workloads/counter.yaml sfr-89f36610-ce71-4440-abe5-12d40b0cb4a1@eu-west-3'
            echo "Deploying blockchain..."
            # TODO check if correct
            timeout 35 ssh ubuntu@$1 './bin/minion run -vv --breakpoint=chain quorum-ibft ../../workloads/counter.yaml '"@$fleet_id"
            # connect in ssh to launch the blockchain
            # timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
            echo "Blockchain deployed"
            # open 2 ssh connections to launch primary and secondary
            echo "Launching primary"
            # TODO check if correct paths for arguments
            ssh ubuntu@$1 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary --env=accounts=install/geth-accounts/accounts.yaml --output=out.txt --env=contracts=contracts  --port=9000 -vvv --stat 1 setup.yaml workload.yaml; ' &
            sleep 5
            echo "Launching secondary"
            ssh ubuntu@$1 './install/diablo/diablo secondary -vvv --port=9000 --tag=any ' $1 &
            wait
            echo "Done with primary and secondary"
            # copy the results from the primary to the local machine
            scp ubuntu@$1:out.txt ~/ml_on_blockchain/results/aws/varying_workers/constant_time/model_length_$model_length/run_$i/
            mv ~/ml_on_blockchain/results/aws/varying_workers/constant_time/model_length_$model_length/run_$i/out.txt /home/user/ml_on_blockchain/results/aws/varying_workers/constant_time/model_length_$model_length/run_$i/$num_workers.txt
            # touch /home/user/ml_on_blockchain/results/varying_workers/constant_time/model_length_$model_length/run_$i/$num_workers.txt

            # kill the blockchain: close all geth instances in parallel
            # iterate over "$@" from second element


            ./stop_blockchain.sh "$@"
            # for ssh_port in {2233..2236}; do
            #     ssh user@dclbigmem.epfl.ch -p $ssh_port "pgrep geth | xargs kill -9" && echo "Closed geth instance on: $ssh_port" &
            # done
            # wait
            # wait 10 secondes
            echo "Waiting 10 seconds before restarting the blockchain"
            sleep 10
            num_workers=$((num_workers * 2))
        done
    done
done
echo "Done"
