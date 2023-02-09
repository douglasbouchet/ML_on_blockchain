#!/bin/bash

# this script expect the number of workers as argument
if [ $# -ne 3 ]; then
    echo "Wrong number of arguments"
    echo "Usage: $0 <number of workers> <Model length> <pace>"
    exit 1
fi

n_workers=$1
model_length=$2
pace=$3

n_chunks=$(echo "0.001 * $model_length" | bc)
total_training_time=$(echo "$n_chunks * $pace" | bc)
n_chunks_per_second=$(echo "$n_workers * $n_chunks / $total_training_time" | bc)

echo "Number of workers: $n_workers"
echo "Model length: $model_length"
echo "Pace: $pace"
echo "Number of chunks: $n_chunks"
echo "Total training time: $total_training_time"
echo "Number of chunks per second: $n_chunks_per_second"


# convert total_training_time into integer
total_training_time=${total_training_time%.*}

slot_duration_addNewEncryptedModel=5

# each worker has model_length/1000 txs to send for addVerificationParameters
worker_number_call_addNewEncryptedModel_per_second=$(($n_workers/$slot_duration_addNewEncryptedModel))
# if less than 1 tx per second, we set it to 1
if [ $worker_number_call_addNewEncryptedModel_per_second -lt 1 ]; then
    worker_number_call_addNewEncryptedModel_per_second=1
fi

# sum of the two slots
start_time_verification=$(($slot_duration_addNewEncryptedModel+1))
end_time_verification=$(($start_time_verification+$total_training_time))

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
            $start_time_verification: $n_chunks_per_second
            $end_time_verification: 0


EOF
