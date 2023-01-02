#!/bin/bash

# Read in a string from the user
read -p "Enter a scenario name: " scenario

echo "Scenario: $scenario"

num_workers=1

# Iterate 5 times
for i in {1..3}; do

    # Multiply the variable by 10
    num_workers=$((num_workers * 10))
    # create file names as number_of_workers and scenario (to save results)
    file_name="$scenario"_"$num_workers"_workers
    touch res/$file_name.txt
    # create the workload.yaml file for the given number of workers and upload it
    # TODO
    # Print the variable
    echo "Testing blockchain with $num_workers workers"
    echo "Deploying blockchain..."
    # connect in ssh to launch the blockchain
    timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
    echo "deployed blockchain"
    # open 2 ssh connections to launch primary and secondary
    ssh user@dclbigmem.epfl.ch -p 2232 'export PATH=$PATH:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --output=out.txt --stat --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=workloads/solidity-contracts/ 1 deploy/diablo/primary/setup.yaml workloads/counter.yaml; ' &
    # wait 5 seconds that primary is launched and then launch secondary
    sleep 5
    ssh user@dclbigmem.epfl.ch -p 2232 "/home/user/diablo/diablo secondary -vvv localhost" &
    sleep 60
    # copy the results from the primary to the local machine
    scp user@dclbigmem.epfl.ch:out.txt res/
    mv res/out.txt res/$file_name.txt
    # kill the blockchain
    echo -e "\n"

    # close all geth instances in parallel
    for ssh_port in {2233..2236}; do
        ssh user@dclbigmem.epfl.ch -p $ssh_port "pgrep geth | xargs kill -9" && echo "Closed geth instance on: $ssh_port" &
    done
    wait
    echo -e "\n"
done
