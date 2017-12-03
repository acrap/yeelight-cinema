#!/usr/bin/python

import pyscreenshot as ImageGrab
from colorthief import ColorThief
from yeelight import Bulb
import io
from PIL import Image
from PIL import ImageFilter
import sys

diff = 25

if __name__ == '__main__':
    # grab fullscreen

    width = 64
    height = 64
    key_color = None

    bulb = Bulb("192.168.1.247", effect="smooth")
    bulb.start_music(2000)

    while True:

        im = ImageGrab.grab()
        # TODO support custom resolutions for primary and second screen
        if len(sys.argv) > 1:
            if sys.argv[1] == 'lg':
                cropped = im.crop((1920, 0+500, 1920+1300, 720+300))
            else:
                cropped = im.crop((0, 0, 1920, 1080))
        else:
            cropped = im.crop((im.size[0] / 3 - 200, im.size[1] / 2 - 200, im.size[0] / 3, im.size[1]))

        resized_img = cropped.resize((width, height), Image.BILINEAR)
        output = io.BytesIO()
        blurred_image = resized_img.filter(ImageFilter.GaussianBlur(radius=5))
        blurred_image.save(output, format='PNG')
        color_thief = ColorThief(output)

        # get the dominant color
        dominant_color = color_thief.get_color(quality=1)

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



