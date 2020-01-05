#!/usr/bin/env python3

""" This tool hides an image inside another image by
storing the most significant bits inside the least
significant bits.

Usage: ./this.py <filename of target> <filename of image to hide>
"""

import numpy
from PIL import Image

def hide_image(stack, needle, n=1):
    """ Hides the needle in the stack and stores the result in the file called 'dest'.
    Uses the lowest n bits in the stack to hide uppest n bits of the needle.
    """

    destination_data = []
    merge = lambda dst, src: (dst & (0xff ^ (0xff >> (8 - n)))) | (src >> (8 - n))

    for row_stack, row_needle in zip(stack, needle):
        new_row = []

        for pixel_stack, pixel_needle in zip(row_stack, row_needle):
            new_pixel = [merge(vs, vn) for vs, vn in zip(pixel_stack, pixel_needle)]
            new_row.append(new_pixel)

        destination_data.append(new_row)

    return destination_data

def read_image(filename):
    """ Reads an image from a file into an array.

    The matplotlib function (https://matplotlib.org/3.1.1/_modules/matplotlib/image.html#imread)
    is not used here since floats for pixel values (used when opening a PNG file) are annoying.
    """

    from matplotlib.image import pil_to_array

    with Image.open(filename) as image:
        return pil_to_array(image)

def main():
    """ Reads the given images into memory, performs the hiding operation and stores the
    result as new image.
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="filename of image to store the output")
    parser.add_argument("stack", help="filename of image to hide data into")
    parser.add_argument("needle", help="filename of payload")
    parser.add_argument("-n", help="number of bits beeing used to hide data",
                        type=int, default=1, choices=range(1, 9))
    args = parser.parse_args()

    print(f"[+] stack = '{args.stack}', needle = '{args.needle}'")
    print(f"[+] use {args.n} bits to hide data")

    image_stack = read_image(args.stack)
    image_needle = read_image(args.needle)

    if image_stack.size != image_needle.size:
        print("[!] sizes of stack and needle are different. Abort.")
        return

    print("[+] hide needle in stack")
    new_data = hide_image(image_stack, image_needle, args.n)

    print("[+] storing hidden image in:", args.output)
    img = Image.fromarray(numpy.array(new_data).astype('uint8'))
    img.save(args.output)

if __name__ == "__main__":
    main()
