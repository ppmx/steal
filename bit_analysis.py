#!/usr/bin/env python3

"""
This module computes 8 images for a given input image where each bit for all
pixels are extracted and visualized.

Usage: ./this.py <filename>
"""

import matplotlib.pyplot as plt

def pixel_bitshift(pixel, n):
    """ Shifts a specific bit (the nth one, starting at 0 to 7) for each value of a pixel to the
    most significant position.
    """

    shift = lambda v: ((v & (0xff >> (7 - n))) << (7 - n))
    return list(map(shift, pixel))

def image_pixel_manipulation(img, f):
    """ Applies the given function f (expecting a pixel and returning a pixel) onto each
    pixel of the given input image img. Returns a new image.
    """

    return [[f(pixel) for pixel in row] for row in img]

def create_grid(img, show_original=True):
    """ Creates a grid and returns the figure and a list of subplots.

    If show_original was set to true then also the original image is shown.
    """

    if not show_original:
        fig, subs = plt.subplots(2, 4)
        subplots = list(subs[0]) + list(subs[1])

        return fig, subplots

    fig = plt.figure()

    subplots = [
        plt.subplot2grid((2, 6), (0, 2), fig=fig),
        plt.subplot2grid((2, 6), (0, 3), fig=fig),
        plt.subplot2grid((2, 6), (0, 4), fig=fig),
        plt.subplot2grid((2, 6), (0, 5), fig=fig),

        plt.subplot2grid((2, 6), (1, 2), fig=fig),
        plt.subplot2grid((2, 6), (1, 3), fig=fig),
        plt.subplot2grid((2, 6), (1, 4), fig=fig),
        plt.subplot2grid((2, 6), (1, 5), fig=fig),

        plt.subplot2grid((2, 6), (0, 0), rowspan=2, colspan=2, fig=fig),
    ]

    subplots[-1].imshow(img)
    subplots[-1].set_title("Original")

    return fig, subplots


def visualize_bitdepth(img):
    """ Opens a new window using pyplot showing an image for each bitdepth. """

    fig, subplots = create_grid(img, show_original=False)
    fig.suptitle("Bit Analysis")

    for i in range(8):
        print("[+] preparing for bit:", i)

        img_modified = image_pixel_manipulation(img, lambda p: pixel_bitshift(p, i))

        subplots[i].imshow(img_modified)
        subplots[i].set_title(f"Bit #{i}")

    fig.subplots_adjust(hspace=0.5)
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
    """ Reads the given filename from the command line passed as
    argument, opens the image and processes it.
    """

    from sys import argv

    try:
        filename = argv[1]
    except IndexError:
        print("Usage:", argv[0], "<filename>")
        return

    # Read and process image:
    img = read_image(filename)
    visualize_bitdepth(img)


if __name__ == "__main__":
    main()
