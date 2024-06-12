# Themer
A program for automatically generating color-themes using an image as a reference.

## Requirements
### For running main script:
Requires the python PILLOW library.

### For automatically running on changed background:
Requires inotifytools for the bash scripts

## Install
Clone the repo, change the output of the themer_conf.py file to suit your needs, you can also add more outputs. Then run
> python main.py [path to image]

in the terminal of the cloned directory.

The current script that monitors for a change in background image does so through inotifytools. This script monitors for when an image in the directory or its subdirectories supplied in the script is accesed. The script will then run main.py in the Themer directory. To use this script one will need to specify the path to the directory where one stores their wallpapers as well as the path to the on_wallpaper_change.sh script. Lastly one needs to add the script as a startup script.

For each file that is outputted into (specified in themer_conf.py), one also needs to send the corresponding signal to all instances that are active, my way of doing this for kitty can be seen in on_wallpaper_change.sh, however i have not found a way of successfully doing so for codium or other applications yet.

## Problems
Doesnt work as good with brighter images (arguably).
The script should run into errors if there are fewer colors in the provided image than there are being asked for or if the colors in the image are to close. 
Note that the automation script will also be triggered when you access an image in the specified directory, this is a drawback of the script that one will have to stand if one doesn't write their own or modify this one. The reason it has been done this way is to offer a script that is as universal as possible, when different WMs and DEs handle wallpapers differently.


## Tinkering
Without really changing any of the code you can tinker with the "themer_conf.py" file to control for example how far away colors must be from each other or how big steps to take when loading pixels.
