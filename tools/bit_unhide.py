#!/usr/bin/env python3

""" This script recovers a hidden image. It extracts the lowest n bits and
stores them as most significant bits.
"""

from PIL import Image

def reveal_lsb(pixel, n):
    """ Extracts the lowest n bits of each pixel value and
    shifts them to the MSB position.
    """

    shift = lambda v: (v & (0xff >> (8 - n))) << (8 - n)
    return list(map(shift, pixel))

def image_pixel_manipulation(img, f):
    """ Applies the given function f (expecting a pixel and returning a pixel) onto each
    pixel of the given input image img. Returns a new image.
    """

    return [[f(pixel) for pixel in row] for row in img]

def store_image(filename, data):
    import numpy

    d = numpy.array(data).astype('uint8')
    Image.fromarray(d).save(filename)

def read_image(filename):
    """ Reads an image from a file into an array.

    The matplotlib function (https://matplotlib.org/3.1.1/_modules/matplotlib/image.html#imread)
    is not used here since floats for pixel values (used when opening a PNG file) are annoying.
    """

    from matplotlib.image import pil_to_array

    with Image.open(filename) as image:
        return pil_to_array(image)

def main():
    """ Reads the given image into memory, extracts the lowest n bits and stores them
    as another image.
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="filename of image to store the output")
    parser.add_argument("input", help="filename of image where hidden data is stored")
    parser.add_argument("-n", help="number of bits beeing used to hide data",
                        type=int, default=1, choices=range(1, 9))
    args = parser.parse_args()

    transformation = lambda pixel: reveal_lsb(pixel, args.n)

    print("[+] read image", args.input)
    img = read_image(args.input)

    print("[+] extract", args.n, "bits")
    new_img = image_pixel_manipulation(img, transformation)

    print("[+] store result in", args.output)
    store_image(args.output, new_img)


if __name__ == "__main__":
    main()
