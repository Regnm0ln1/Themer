#!/bin/bash

python [] $1 > ~/.config/kitty/current-theme.conf

# Get the process IDs of all running Kitty instances
kitty_pids=$(pgrep -x kitty)
echo $kitty_pids

# Send SIGUSR1 to each Kitty process to reload the configuration
for pid in $kitty_pids; do

    kill -SIGUSR1 "$pid"
done