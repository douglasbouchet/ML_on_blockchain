#!/bin/bash

# this script expect the number of workers as argument
if [ $# -ne 2 ]; then
    echo "Wrong number of arguments"
    echo "Usage: $0 <number of workers> <Model length>"
    exit 1
fi

n_workers=$1
model_length=$2
# the time we allow to send the addVerificationParameters transaction. Based on 100k model length
# base_verification_duration=40
# Upon working on 100k model length, each worker has 100 txs of 1000 weights to send.
# we assume that each worker send a new txs every second -> expected time to send all txs is 100s i.e time to perform one learning step
base_verification_duration=100
slot_duration_addNewEncryptedModel=5
# we compute the adapted verification duration based on the model length
#verification_duration=$(($base_verification_duration*$model_length/100000))
verification_duration=$(($base_verification_duration*$model_length/100000))
# if verification_duration is lower than 40, we set it to 40
if [ $verification_duration -lt 40 ]; then
    verification_duration=40
fi
# each worker has model_length/1000 txs to send for addVerificationParameters
worker_number_call_addNewEncryptedModel_per_second=$(($n_workers/$slot_duration_addNewEncryptedModel))
# if less than 1 tx per second, we set it to 1
if [ $worker_number_call_addNewEncryptedModel_per_second -lt 1 ]; then
    worker_number_call_addNewEncryptedModel_per_second=1
fi
worker_number_call_verification_parameters_per_second=$(($n_workers*$model_length/(1000*$verification_duration)))
# the addNewEncryptedModel slot for sending txs is the same
echo "Number of workers: $n_workers"
echo "model length: $model_length"
echo "Verification duration: $verification_duration"
echo "Number of calls to addNewEncryptedModel: $worker_number_call_addNewEncryptedModel_per_second"
echo "Number of calls to addVerificationParameters: $worker_number_call_verification_parameters_per_second"

# sum of the two slots
start_time_verification=$(($slot_duration_addNewEncryptedModel+1))
end_time_verification=$(($start_time_verification+$verification_duration))

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
            function: "addNewEncryptedModel()"
          load:
            0: $worker_number_call_addNewEncryptedModel_per_second
            $slot_duration_addNewEncryptedModel: 0
        - interaction: !invoke
            from: *account
            contract: *contract
            function: "addVerificationParameters()"
          load:
            $start_time_verification: $worker_number_call_verification_parameters_per_second
            $end_time_verification: 0


EOF

cp generated/workload.yaml /home/user/ml_on_blockchain/workload/federated_learning.yaml
