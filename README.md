# Themer
A program for automatically generating color-themes using an image as a reference, mainly for kitty

## Install
Clone the repo, change the IMAGE_PATH in the color_distance.py file to your desired image, then run 
> python color_distance.py

in the terminal when in the cloned directory.
Put the output in you kitty.conf file (if it's for kitty ofcourse)

## Problems
Currently doesn't support specifying dark or bright background
Doesnt work as good with brighter images
Currently working on a way to automatically change theme on automatically changing backgorund images

## Tinkering
Without really changing any of the code you can tinker with the "min_color_dist" variable to controll the contrast between backgroundcolor and the other colors
You can also change things in the score_colors function
