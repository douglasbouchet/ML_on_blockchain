#!/bin/bash

# this script expect the number of workers as argument
if [ $# -ne 1 ]; then
    echo "Wrong number of arguments"
    echo "Usage: $0 <number of workers>"
    exit 1
fi

n_workers=$1
# we divide the number of workers by 10 to get number of call to smart contract to make per second
n_calls_per_second=$((n_workers/10))
echo "Number of workers: $n_workers"
echo "Number of calls per second: $n_calls_per_second"

cat <<EOF > generated/workload.yaml
let:
  - !loop &account
    sample: !account
      number: 100
      stake: 10000000
  - !loop &any_location
    sample: !location
      - ".*"
  - !loop &any_endpoint
    sample: !endpoint
      - ".*"
  - &contract
    sample: !contract
      number: 1
      name: "learn_task"
workloads:
  - number: 1
    client:
      location: *any_location
      view: *any_endpoint
      behavior:
        - interaction: !invoke
            from: *account
            contract: *contract
            function: "getModelAndBatchIndex()"
          load:
            0: $n_calls_per_second
            10: 0
        - interaction: !invoke
            from: *account
            contract: *contract
            function: "addNewEncryptedModel()"
          load:
            0: $n_calls_per_second
            10: 0
        - interaction: !invoke
            from: *account
            contract: *contract
            function: "addVerificationParameters()"
          load:
            15: $n_calls_per_second
            25: 0
EOF
