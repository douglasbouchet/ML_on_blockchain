for ip in "$@"; do
    ssh ubuntu@$ip "pgrep geth | xargs kill -9" && echo "Closed geth instance on: $ip" &
done
wait
