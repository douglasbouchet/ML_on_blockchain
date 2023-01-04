#!/bin/bash

# expect a list of ip addresses as arguments. First one is primary address and the rest are secondary addresses
if [ $# -lt 2 ]
then
    echo "Error: Need provide at least 2 IP addresses"
    exit 1
fi

# Read in a string from the user
read -p "Enter a scenario name: " scenario

echo "Scenario: $scenario"

# count the number of arguments
num_args=$#
# subtract 1 to get the number of secondary addresses
num_secondary=$((num_args - 1))
echo "Number of secondary addresses: $num_secondary"

# connect to primary and launch diablo primary
# ssh user@dclbigmem.epfl.ch -p 2232 'export PATH=/home/user/.local/bin:/home/user/anaconda3/bin:/home/user/anaconda3/condabin:/home/user/solidity/build/solc:/home/user/diablo:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/user/solidity/build/solc/ ; /home/user/diablo/diablo primary -vvv --output=out.txt --stat --env=accounts=deploy/diablo/primary/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ 1 deploy/diablo/primary/setup.yaml ml_on_blockchain/workload/federated_learning_generated.yaml; ' &
ssh user@$1 'export PATH=install/solidity/build/solc/:$PATH; ./install/diablo/diablo primary --env=accounts=install/geth-accounts/accounts.yaml --env=contracts=ml_on_blockchain/smart-contracts/federatedLearning/ --port=3000 -vvv --stat '"$num_secondary"' setup.yaml workload.yaml; ' &
# wait 5 seconds that primary is launched and then launch secondary
sleep 5
# connect to each secondary and launch diablo secondary
for var in "${@:2}";do
    ssh user@$var './install/diablo/diablo secondary -vvv --port=3000 --tag=any ' $1 &
done
wait
# copy the result file from primary to local machine
scp user@$1:out.txt res/
mv res/out.txt res/$scenario/$file_name.txt
echo -e "\n"

# end machine: see if sufficient to just kill all geth processes
# TODO
