#!/usr/bin/env bash

# Read the JSON from out.txt
filename=$1
json=$(cat $filename)

# Use jq to parse the JSON
submitted=$(echo "$json" | jq '.Locations[0].Clients[0].Interactions | length')
commits=$(echo "$json" | jq '.Locations[0].Clients[0].Interactions | map(select(.CommitTime != -1)) | length')

# Initialize total_time to 0
total_time=0
total_submit_time=0

# iterate over each interaction and print its content
echo "$json" | jq '.Locations[0].Clients[0].Interactions | .[]' | while read interaction; do
    # echo "$interaction" |grep "CommitTime"
    echo "$interaction"
    result=$(echo "$interaction" | grep "CommitTime")
    if [ -z "$result" ]; then
        # submit_time=$(echo "$interaction" | grep "SubmitTime" | awk '{print $2}' | sed 's/\"//g' | sed 's/,//g')
        # # check if submit_time is not empty
        # if [ -z "$submit_time" ]; then
        #     continue
        # else
        #     total_submit_time=$(echo "$total_submit_time + $submit_time" | bc)
        # fi
        continue
    else
        commit_time=$(echo "$result" | awk '{print $2}' | sed 's/\"//g' | sed 's/,//g')
        # if commit_time != -1
        if [ "$commit_time" != "-1" ]; then
            total_time=$(echo "$total_time + $commit_time" | bc)
        fi
    fi
    done
echo "total_submit_time: $total_submit_time"
echo "total_time: $total_time"

# Iterate over each interaction and add its commit time to total_time
echo "$json" | jq '.Locations[0].Clients[0].Interactions | map(select(.CommitTime != -1)) | .[] | .CommitTime' | while read commit_time; do
  total_time=$(echo "$total_time + $commit_time" | bc)
done

# Calculate the average commit time
average_time=$(echo "scale=2; $total_time / $commits" | bc)

# Output the results
echo "Submitted: $submitted"
echo "Commits: $commits"
echo "Average time to commit: $average_time"
