#!/usr/bin/env python3

""" This module computes and shows each color channel (red/green/blue)
using the matploblib and pillow.
"""

import matplotlib.pyplot as plt
import numpy

def show_rgb_channel(img):
    """ Shows a grid of eight images for each bit in the pixels """

    figure, subplots = plt.subplots(1, 3)

    figure.suptitle("Color Channels")

    channels = {c: numpy.zeros(img.shape, dtype=int) for c in ["red", "green", "blue"]}

    for index, (name, channel) in enumerate(channels.items()):
        channel[:, :, index] = img[:, :, index]
        subplots[index].imshow(channel)
        subplots[index].set_title(name)

    figure.subplots_adjust(hspace=0.5)
    plt.show()

def read_image(filename):
    """ Reads an image from a file into an array.

    The matplotlib function (https://matplotlib.org/3.1.1/_modules/matplotlib/image.html#imread)
    is not used here since floats for pixel values (used when opening a PNG file) are annoying.
    """

    from PIL import Image
    from matplotlib.image import pil_to_array

    with Image.open(filename) as image:
        return pil_to_array(image)

def main():
    """ Usage:

    $ ./this.py <filename>
    """

    from sys import argv

    try:
        filename = argv[1]
    except IndexError:
        print("Usage:", argv[0], "<filename>")
        return

    img = read_image(filename)
    show_rgb_channel(img)

if __name__ == "__main__":
    main()
