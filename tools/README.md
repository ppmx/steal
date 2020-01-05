# STEAL tools

Here are some tools to perform steganographic operations. For testing purpose.


## Script `msb.py`

Restricts an image to the upper n bits. Can be used as preview tool for an image that will be restricted to its n lowest bits in order to hide it into another image.

### Example
```
$ python3 msb.py -n 2 /tmp/msb_output.png ../tests/circles/needle.png
```


## Script `bit_hide.py`

Hides an image by storing its n most significant bits inside the n lowest significant bits.

### Example:
```
$ python3 bit_hide.py -n 2 /tmp/enigma.png ../tests/circles/stack.png /tmp/msb_output.png
```


## Script `bit_unhide.py`

The script `bit_unhide.py` recovers the hidden image. It extracts the lowest n bits and stores them as most significant bits.

### Example:
```
$ python3 bit_unhide.py -n 2 /tmp/revealed.png /tmp/enigma.png
```
