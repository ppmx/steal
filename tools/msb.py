#!/usr/bin/env python3

import argparse
import numpy
from PIL import Image

def read_image(filename):
    """ Reads an image from a file into an array.

    The matplotlib function (https://matplotlib.org/3.1.1/_modules/matplotlib/image.html#imread)
    is not used here since floats for pixel values (used when opening a PNG file) are annoying.
    """

    from matplotlib.image import pil_to_array

    with Image.open(filename) as image:
        return pil_to_array(image)

def main():
    """ Example:

    $ python3 msb.py -n 2 /tmp/msb_output.png ../tests/circles/needle.jpeg
    """

    parser = argparse.ArgumentParser(description="Tool to restrict image data to the upper n bits")
    parser.add_argument("output", help="filename of image to store the output")
    parser.add_argument("input", help="filename")
    parser.add_argument("-n", help="number of bits beeing used to hide data", type=int, default=1, choices=range(1, 9))
    args = parser.parse_args()

    # transformation for one pixel. cuts the lowest bits to restrict pixel values to the
    # upper n bits:
    mask = 0xff ^ (0xff >> args.n)
    transform = lambda pix: list(map(lambda v: v & mask, pix))

    # Read image, perform pixel substitution and store the image:
    img = read_image(args.input)
    new_data = [[transform(pixel) for pixel in col] for col in img]
    Image.fromarray(numpy.array(new_data).astype('uint8')).save(args.output)

if __name__ == "__main__":
    main()
