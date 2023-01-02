#!/bin/sh
# Check that at least one IP address has been provided as an argument
if [ $# -lt 1 ]
then
    echo "Error: No IP addresses provided"
    echo "Call example: ./setup-vm.sh 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi


# create the setup.yaml file for the given ip addresses
./create_setup.sh @

# check that the setup.yaml file has been created
if [ ! -f setup.yaml ]
then
    echo "Error: setup.yaml file not found"
    exit 1
fi
# check that workload.yaml exists
if [ ! -f workload.yaml ]
then
    echo "Error: workload.yaml file not found"
    exit 1
fi

timeout=5 # if the connection is not established within 5 seconds, exit with an error message

for var in "$@" # read the list of ip addresses

    # Use scp to copy the file to the remote IP address, and exit with an error message if nothing happens after 5 seconds
    if ! scp -o ConnectTimeout=$timeout workload.yaml user@$var:~; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: user@$var is reachable."
      exit 1
    fi
    echo "sent workload.yaml to user@$var"
    if ! scp -o ConnectTimeout=$timeout setup.yaml user@$var:~; then
      echo "Error: scp failed to connect within $timeout seconds. Verify that address: user@$var is reachable."
      exit 1
    fi
    echo "sent setup.yaml to user@$var"
done
