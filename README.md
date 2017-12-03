# yeelight-cinema
This python script can be used with yeelight color bulb.
Script detects color of scene and changes bulb color.

How to use:
Enable direction by local network in Yeelight application (Android/iOs)
Run script without arguments and it will calculates dominant color on screen and changes bulb color.

TODO:
This script supports only Full Hd primary monitor now. Need to remove hardcoded resolutions and support custom settings.
Script uses too much memory. Need to decrease it.
There are big delays between scene change and bulb reaction. Need to investigate how to decrease it.
Use argparse module to support more arguments and commands.
