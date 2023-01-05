#!/bin/bash

# expect a list of ip addresses as arguments. First one is primary address and the rest are secondary addresses
if [ $# -lt 2 ]
then
    echo "Error: Need provide at least 2 IP addresses"
    exit 1
fi

# Read in a string from the user
read -p "Enter a scenario name: " scenario
read -p "Enter the number of workers: " num_workers

echo "Scenario: $scenario"
echo "Number of workers: $scenario"

# setup file for results
file_name="$num_workers"_workers
mkdir res/$scenario
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
