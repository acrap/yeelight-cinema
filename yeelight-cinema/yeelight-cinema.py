#!/usr/bin/python

import pyscreenshot as image_grab
import threading
from yeelight import Bulb
from PIL import Image
import sys
import argparse
from queue import Queue

exit_signal_received = False


def bulb_setter_thread(bulb_param, queue):
    try:
        while not exit_signal_received:
            if isinstance(queue, Queue):
                try:
                    color = queue.get(timeout=5)
                except:
                    continue
                if isinstance(color, list):
                    if isinstance(bulb_param, Bulb):
                        try:
                            bulb_param.set_rgb(color[0], color[1], color[2])
                        except:
                            pass
    except KeyboardInterrupt:
        pass

def string_to_resolution_list(resolution_str):
    try:
        width = int(resolution_str[:resolution_str.index('x')])
        heihgt = int(resolution_str[resolution_str.index('x')+1:])
    except:
        print("invalid resolution '{0}'. Use WIDTHxHEIGHT format (for example 1920x1080)".format(resolution_str))
        sys.exit(-1)
    res_list = [width, heihgt]
    return res_list


def terminate_handler(bulb_param):
    global exit_signal_received
    if isinstance(bulb, Bulb):
        try:
            bulb_param.stop_music()
        except:
            pass
    exit_signal_received = True


if __name__ == '__main__':
    width = 32*16
    height = 32*9

    queue = Queue(maxsize=1)

    parser = argparse.ArgumentParser(description="yeelight color bulb cinema mode script")

    parser.add_argument("--target_screen", "-ts", default='left', type=str)
    parser.add_argument("--resolution_l", "-rl", default='1920x1080')
    parser.add_argument("--resolution_r", "-rr", default='1360x768')
    parser.add_argument("--bulb_ip", "-bip", default='192.168.1.247')
    parser.add_argument("--color_diff", "-cdiff", default='25')
    parser.add_argument("--bulb_effect", "-bef", default='smooth')

    args = parser.parse_args()
    diff = int(args.color_diff)

    first_screen_res = string_to_resolution_list(args.resolution_l)
    second_screen_res = string_to_resolution_list(args.resolution_r)

    key_color = None

    bulb = Bulb(args.bulb_ip, effect=args.bulb_effect)
    bulb.start_music(2000)
    bbox = (0, 0, first_screen_res[0], first_screen_res[1])

    if args.target_screen.startswith("right"):
        bbox = (first_screen_res[0],
                first_screen_res[1] - second_screen_res[1],
                first_screen_res[0] + second_screen_res[0],
                first_screen_res[1])

    t = threading.Thread(name="bulb_color_change_thread", target=bulb_setter_thread, args=(bulb, queue,))
    t.start()

    while not exit_signal_received:
        try:
            im = image_grab.grab(bbox=bbox)
            resized_img = im.resize((width, height), Image.BILINEAR)
            resize = 150
            result = resized_img.convert('P', palette=Image.ADAPTIVE, colors=1)
            colors = result.getpalette()
            dominant_color = colors[0:3]
            if key_color is None:
                key_color = dominant_color
            else:
                if abs(dominant_color[0] - key_color[0]) < diff\
                    and abs(dominant_color[1] - key_color[1]) < diff \
                        and abs(dominant_color[2] - key_color[2]) < diff:
                    continue
                else:
                    key_color = dominant_color

            queue.put([dominant_color[0], dominant_color[1], dominant_color[2]])

        except KeyboardInterrupt:
            terminate_handler(bulb)
        except Exception as e:
            print("Exception: ", e)
