#!/usr/bin/python

import pyscreenshot as image_grab
from colorthief import ColorThief
from yeelight import Bulb
import io
from PIL import Image
from PIL import ImageFilter
import sys
import argparse


def string_to_resolution_list(resolution_str):
    try:
        width = int(resolution_str[:resolution_str.index('x')])
        heihgt = int(resolution_str[resolution_str.index('x')+1:])
    except:
        print "invalid resolution '{0}'. Use WIDTHxHEIGHT format (for example 1920x1080)".format(resolution_str)
        sys.exit(-1)
    res_list = [width, heihgt]
    return res_list


if __name__ == '__main__':
    width = 64
    height = 64

    parser = argparse.ArgumentParser(description="yeelight color bulb cinema mode script")

    parser.add_argument("--screen", "-s", default='left')
    parser.add_argument("--resolution_l", "-rl", default='1920x1080')
    parser.add_argument("--resolution_r", "-rr", default='1360x768')
    parser.add_argument("--bulb_ip", "-bip", default='192.168.1.247')
    parser.add_argument("--color_diff", "-cdiff", default='25')

    args = parser.parse_args()
    diff = int(args.color_diff)

    first_screen_res = string_to_resolution_list(args.resolution_l)
    second_screen_res = string_to_resolution_list(args.resolution_r)

    key_color = None

    bulb = Bulb(args.bulb_ip, effect="smooth")
    bulb.start_music(2000)
    output = io.BytesIO()
    while True:

        im = image_grab.grab()
        if len(sys.argv) > 1:
            if args.screen == 'right':
                cropped = im.crop((first_screen_res[0],
                                   first_screen_res[1] - second_screen_res[1],
                                   first_screen_res[0] + second_screen_res[0],
                                   first_screen_res[1]))
            else:
                cropped = im.crop((0, 0, first_screen_res[0], first_screen_res[1]))
        else:
            cropped = im.crop((0, 0, first_screen_res[0], first_screen_res[1]))

        resized_img = cropped.resize((width, height), Image.BILINEAR)

        blurred_image = resized_img.filter(ImageFilter.GaussianBlur(radius=5))
        output.flush()
        output.seek(0, 0)
        blurred_image.save(output, format='PNG')
        try:
            color_thief = ColorThief(output)
            dominant_color = color_thief.get_color(quality=10)
        except Exception:
            print "exception"

        if key_color is None:
            key_color = dominant_color
        else:
            if abs(dominant_color[0] - key_color[0]) < diff\
                and abs(dominant_color[1] - key_color[1]) < diff \
                    and abs(dominant_color[2] - key_color[2]) < diff:
                continue
            else:
                key_color = dominant_color
        bulb.set_rgb(dominant_color[0], dominant_color[1], dominant_color[2])




