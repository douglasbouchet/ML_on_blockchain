#!/bin/sh
for var in "$@" # read the list of ip addresses
do
    scp workload.yaml user@$var:~ # copy the workload.yaml file to the remote machine
    echo "sending workload.yaml to user@$var"
    scp setup.yaml user@$var:~ # copy the setup.yaml file to the remote machine
    echo "sending setup.yaml to user@$var"
done
