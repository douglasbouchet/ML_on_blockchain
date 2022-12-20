#!/bin/bash

# Check that at least one IP address has been provided as an argument
if [ $# -lt 1 ]
then
    echo "Error: No IP addresses provided"
    echo "Call example: ./create_setup.sh 192.168.201.3 192.168.201.4 192.168.201.5 192.168.201.6"
    exit 1
fi

# Set the port number to 3000
port=3000

# Initialize the list of IP addresses with port numbers
addresses=()
for ip in "$@"
do
    addresses+=("$ip:$port")
done

# Create the yaml file
cat > setup.yaml <<EOF
interface: "ethereum"

parameters:
  confirm: polltx
  prepare: signature

endpoints:

  - addresses:
EOF

# Add the list of IP addresses with port numbers to the yaml file
for address in "${addresses[@]}"
do
    echo "      - $address" >> config.yaml
done

# Add the tags to the yaml file
echo "    tags:" >> config.yaml
echo "      - vm-dclbigmem-1" >> config.yaml
echo "      - c5.xlarge" >> config.yaml

echo "Yaml file created: config.yaml"
