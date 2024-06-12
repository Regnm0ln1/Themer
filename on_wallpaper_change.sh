#!/bin/bash

python ~/Documents/projects/Themer/main.py $1

# Get the process IDs of all running Kitty instances
kitty_pids=$(pgrep -x kitty)
echo $kitty_pids

codium_pids=$(pgrep -x codium)
echo $codium_pids

# Send SIGUSR1 to each Kitty process to reload the configuration
for pid in $kitty_pids; do

    kill -SIGUSR1 "$pid"
done
