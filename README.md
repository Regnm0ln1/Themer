# Themer
A program for automatically generating color-themes using an image as a reference.

## Requirements
Requires the python PILLOW library.


## Install
Clone the repo, change the output of the themer_conf.py file to suit your needs, you can also add more outputs. Then run
> python main.py [path to image]

in the terminal of the cloned directory.

There is now also a quick fix for automatically running the script when the wallpaper changes. In the "on_wallpaper_change.sh" script, change "[]" to the path to main.py. This script will run main.py  script which in turn will output the new themes to all the ouputs in the "themer_conf.py" file. Lastly add the "monitor_wallpaper_events.sh" script to "application autostart" in "sessions and startup". It only works with xfce at the moment but I am looking for a more permanent and universal solution. 

## Problems
Currently doesn't support specifying dark or bright background.
Doesnt work as good with brighter images.
Currently working on a way to automatically change theme on automatically changing backgorund images.
The script should run into errors if there are fewer colors in the provided image than there are being asked for or if the colors in the image are to close. 

## Tinkering
Without really changing any of the code you can tinker with the "themer_conf.py" file to control for example how far away colors must be from each other or how big steps to take when loading pixels.
