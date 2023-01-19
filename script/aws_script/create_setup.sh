#!/bin/bash

# Check that at least one IP address has been provided as an argument. These IP's are the IP's of the nodes
if [ $# -lt 1 ]
then
    echo "Error: No IP addresses provided"
    echo "Call example: ./create_setup.sh 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

# Set the port number to 9000 (3k not working)
port=9000

# Initialize the list of IP addresses with port numbers
addresses=()
for ip in "$@"
do
    addresses+=("$ip:$port")
done

# Create the yaml file
cat > generated/setup.yaml <<EOF
interface: "ethereum"

parameters:
  prepare: signature

endpoints:

  - addresses:
EOF

# Add the list of IP addresses with port numbers to the yaml file
for address in "${addresses[@]}"
do
    echo "      - $address" >> generated/setup.yaml
done

# Add the tags to the yaml file
echo "    tags:" >> generated/setup.yaml
echo "      - c5.xlarge" >> generated/setup.yaml

echo "setup.yaml file created"
