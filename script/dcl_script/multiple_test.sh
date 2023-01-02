#!/bin/bash

# Read in a string from the user
read -p "Enter a string: " str

echo "Scenario: $str"

num_workers=1

# Iterate 5 times
for i in {1..1}; do
    # Multiply the variable by 10
    num_workers=$((num_workers * 10))
    # Print the variable
    echo "Testing blockchain with $num_workers workers"
    echo "Deploying blockchain..."
    # connect in ssh to launch the blockchain
    # timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3@vm-dclbigmem-1"
    echo "  deployed blockchain"
    # open 2 ssh connections to launch primary and secondary
    #timeout 80 ssh user@dclbigmem.epfl.ch -p 2232 'echo $PATH; export PATH=$PATH:/home/user/solidity/build/solc/ ; echo $PATH; /home/user/diablo/diablo primary -vvv --stat --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=workloads/solidity-contracts/ 1 deploy/diablo/primary/setup.yaml workloads/counter.yaml' &
    ssh user@dclbigmem.epfl.ch -p 2232 'echo $PATH; export PATH=$PATH:/home/user/solidity/build/solc/ ; echo $PATH; /home/user/diablo/diablo primary -vvv --stat --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=workloads/solidity-contracts/ 1 deploy/diablo/primary/setup.yaml workloads/counter.yaml' &
    # wait 5 seconds that primary is launched and then launch secondary
    sleep 5
    #timeout 80 ssh user@dclbigmem.epfl.ch -p 2232 "/home/user/diablo/diablo secondary -vvv localhost" &
    ssh user@dclbigmem.epfl.ch -p 2232 "/home/user/diablo/diablo secondary -vvv localhost" &
    sleep 60
    exit

done
