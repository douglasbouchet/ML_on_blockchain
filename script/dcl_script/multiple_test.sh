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
    # connect in ssh to launch the blockchain
    # ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/test && touch gg$i.txt"
    # ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3,192.168.203.4,192.168.203.5,192.168.203.6@vm-dclbigmem-1"
    echo "Deploying blockchain..."
    timeout 35 ssh user@dclbigmem.epfl.ch -p 2232 "cd ~/minion && ./bin/minion run -vvv --user=user --breakpoint=chain quorum ../workloads/counter.yaml 127.0.0.1,192.168.203.3@vm-dclbigmem-1"
    echo "deployed blockchain"

done
