# yeelight-cinema
This python script can be used with yeelight color bulb.
Script detects color of scene and changes bulb color.

# How to use:
Enable direction by local network in Yeelight application (Android/iOs)
Run script without arguments and it will calculates dominant color on screen and changes bulb color.

# Installation 

    pip install yeelight-cinema

# Usage:
    yeelight-cinema.py --bulb_ip=192.168.1.240 --resolution_l=1920x1080

To use with secondary monitor (places right):

                                                screen to use    left screen resolution      right screen resolution
    yeelight-cinema.py --bulb_ip=192.168.1.240 --target_screen=right --resolution_l=1920x1080 --resolution_r=1920x1080

# Dependencies:
Pillow, pyscreenshot, colorthief, yeelight

# TODO:
Script uses too much CPU. Need to decrease it.
There are big delays between scene change and bulb reaction. Need to investigate how to decrease it.

