#!/bin/bash

############ Chat GPT made this by the way ############

# Directory to monitor
DIR=~/Pictures/wallpapers

# Variable to store the last accessed file
last_accessed=""

# Infinite loop to keep the script running
while true; do
  # Monitor for access of all files and subdirectories in DIR
  new_wallpaper=$(inotifywait -r -e access --format '%w%f' "$DIR" 2>/dev/null)
  
  # Get the file extension
  extension="${new_wallpaper##*.}"

  # Check if the accessed file is an image (by extension) and if it is different from the last accessed file
  if [[ "$new_wallpaper" != "$last_accessed" && "$extension" =~ ^(jpg|jpeg|png|gif|bmp|tiff|webp)$ ]]; then
    ~/Documents/projects/Themer/on_wallpaper_change.sh "$new_wallpaper"
    last_accessed=$new_wallpaper
  fi

  # sleep 0.5
done
