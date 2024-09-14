#!/bin/bash

python ~/Documents/projects/Themer/main.py $1

# Get the process IDs of all running Kitty instances
kitty_pids=$(pgrep -x kitty)
echo $kitty_pids

cava_pids=$(pgrep -x cava)
echo $cava_pids

# Send SIGUSR1 to each Kitty process to reload the configuration
for pid in $kitty_pids; do

    kill -SIGUSR1 "$pid"
done

for pid in $cava_pids; do
    kill -SIGUSR2 "$pid"
done
