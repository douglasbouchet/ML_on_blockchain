#!/bin/bash

# Read in a string from the user
read -p "Enter a string: " scenario

echo "Scenario: $scenario"

num_workers=1

# Iterate 5 times
for i in {1..1}; do
    # Multiply the variable by 10
    num_workers=$((num_workers * 10))
    # create file names as number_of_workers and scenario (to save results)
    file_name="$scenario"_"$num_workers"_workers
    touch res/$file_name.txt
    # Print the variable
    echo "Testing blockchain with $num_workers workers"
    echo "Deploying blockchain..."
    # connect in ssh to launch the blockchain
    # timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3@vm-dclbigmem-1"
    echo "  deployed blockchain"
    # open 2 ssh connections to launch primary and secondary
    # ssh user@dclbigmem.epfl.ch -p 2232 'export PATH=$PATH:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --stat --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=workloads/solidity-contracts/ 1 deploy/diablo/primary/setup.yaml workloads/counter.yaml' &
    ssh user@dclbigmem.epfl.ch -p 2232 'export PATH=$PATH:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --output=out.txt --stat --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=workloads/solidity-contracts/ 1 deploy/diablo/primary/setup.yaml workloads/counter.yaml; ' &
    # wait 5 seconds that primary is launched and then launch secondary
    sleep 5
    ssh user@dclbigmem.epfl.ch -p 2232 "/home/user/diablo/diablo secondary -vvv localhost" &
    sleep 60
    scp user@dclbigmem.epfl.ch:out.txt res/
    # rename res/out.txt to res/$file_name.txt
    mv res/out.txt res/$file_name.txt
    exit

done
