# Themer
A program for automatically generating color-themes using an image as a reference, mainly for kitty

## Requirements
Requires the python PILLOW library


## Install
Clone the repo, then run
> python color_distance.py [path to image]

in the terminal when in the cloned directory.
Put the output in you kitty.conf file, or where you keep your kitty color configs (if it's for kitty ofcourse)

There is now also a quick fix for automatically running the script on wallpaper change is in the "monitor-wallpaper-events.sh" script, change "[]" to the path to color-distance.py. It only works for xfce at the moment but I am looking for a more permanent and universal fix. This script will add the config to a file called current-theme.conf, this must be linked to from your kitty.conf by writing "include current-theme.conf" at the top of the file.

## Problems
Currently doesn't support specifying dark or bright background
Doesnt work as good with brighter images
Currently working on a way to automatically change theme on automatically changing backgorund images

## Tinkering
Without really changing any of the code you can tinker with the "min_color_dist" variable to controll the contrast between backgroundcolor and the other colors
You can also change things in the score_colors function
