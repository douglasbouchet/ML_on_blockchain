#!/bin/bash

# this script expect the number of workers as argument
if [ $# -ne 2 ]; then
    echo "Wrong number of arguments"
    echo "Usage: $0 <number of workers> <Model length>"
    exit 1
fi

n_workers=$1
model_length=$2
# the time we allow to send the addVerificationParameters transaction. Based on 1M model length
base_verification_duration=20
slot_duration_addNewEncryptedModel=5
# we compute the adapted verification duration based on the model length
verification_duration=$(($base_verification_duration*$model_length/1000000))
# each worker has model_length/1000 txs to send for addVerificationParameters
worker_number_call_addNewEncryptedModel_per_second=$(($n_workers/$slot_duration_addNewEncryptedModel))
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
