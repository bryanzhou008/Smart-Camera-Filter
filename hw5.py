import struct
from functools import reduce
from collections import namedtuple

pixel = namedtuple("pixel", "r g b")

'''
You need to implement the six functions defined below.
Each function takes a single argument:
  an image represented as a list of lists of pixels, where
  each pixel has the type pixel defined above.
Each function returns a list in exactly that same form.

The readPPM and writePPM functions defined at the end of the file should NOT be
called by your code.  Rather, they are provided to help you test your code:
readPPM allows you to convert PPM image files into lists of lists of pixels that
can be passed as arguments to your functions, and writePPM allows you to write the
results of your functions to image files so that the images can be viewed.
'''



def negate(pixels):
    '''newRow = list(map(lambda x:pixel(r=255-x.r, g=255-x.g, b=255-x.b),pixels))'''
    return list(map(negateHelper, pixels))
def negateHelper(row):
    return list(map(lambda x:pixel(r=255-x.r, g=255-x.g, b=255-x.b),row))
def test_negate():
    assert negate([[pixel(r=10, g=23, b=52), pixel(r=82, g=3, b=215)], \
                   [pixel(r=30, g=181, b=101), pixel(r=33, g=45, b=205)], \
                   [pixel(r=40, g=68, b=92), pixel(r=111, g=76, b=1)]])==\
                   [[pixel(r=245, g=232, b=203), pixel(r=173, g=252, b=40)], \
                    [pixel(r=225, g=74, b=154), pixel(r=222, g=210, b=50)], \
                    [pixel(r=215, g=187, b=163), pixel(r=144, g=179, b=254)]]


def greyscale(pixels):
    return list(map(greyscaleHelper, pixels))
def greyscaleHelper(row):
    return list(map(lambda x:pixel(r=int(round(.299*x.r+.587*x.g+.114*x.b)), \
                                   b=int(round(.299*x.r+.587*x.g+.114*x.b)), \
                                   g=int(round(.299*x.r+.587*x.g+.114*x.b))), row))
def test_greyscale():
    assert greyscale([[pixel(r=10, g=23, b=52), pixel(r=82, g=3, b=215)], \
                      [pixel(r=30, g=181, b=101), pixel(r=33, g=45, b=205)], \
                      [pixel(r=40, g=68, b=92), pixel(r=111, g=76, b=1)]])==\
                      [[pixel(r=22, g=22, b=22), pixel(r=51, g=51, b=51)], \
                       [pixel(r=127, g=127, b=127), pixel(r=60, g=60, b=60)], \
                       [pixel(r=62, g=62, b=62), pixel(r=78, g=78, b=78)]]


def upsideDown(pixels):
    return pixels[::-1]
def test_upsideDown():
    assert upsideDown([[pixel(r=10, g=23, b=52), pixel(r=82, g=3, b=215)], \
                       [pixel(r=30, g=181, b=101), pixel(r=33, g=45, b=205)], \
                       [pixel(r=40, g=68, b=92), pixel(r=111, g=76, b=1)]])==\
                       [[pixel(r=40, g=68, b=92), pixel(r=111, g=76, b=1)], \
                        [pixel(r=30, g=181, b=101), pixel(r=33, g=45, b=205)], \
                        [pixel(r=10, g=23, b=52), pixel(r=82, g=3, b=215)]]



def mirrorImage(pixels):
    return list(map(lambda x:x[::-1], pixels))
def test_mirrorImage():
    assert mirrorImage([[pixel(r=10, g=23, b=52), pixel(r=82, g=3, b=215)], \
                        [pixel(r=30, g=181, b=101), pixel(r=33, g=45, b=205)], \
                        [pixel(r=40, g=68, b=92), pixel(r=111, g=76, b=1)]]) ==\
                        [[pixel(r=82, g=3, b=215), pixel(r=10, g=23, b=52)], \
                         [pixel(r=33, g=45, b=205), pixel(r=30, g=181, b=101)], \
                         [pixel(r=111, g=76, b=1), pixel(r=40, g=68, b=92)]]
                        



def compress(pixels):
    halfColumn=list(map(lambda x: x[::2], pixels))
    return halfColumn[::2]
def test_compress():
    assert compress([[pixel(r=10, g=23, b=52), pixel(r=82, g=3, b=215)], \
                     [pixel(r=30, g=181, b=101), pixel(r=33, g=45, b=205)], \
                     [pixel(r=40, g=68, b=92), pixel(r=111, g=76, b=1)]]) ==\
                     [[pixel(r=10, g=23, b=52)], [pixel(r=40, g=68, b=92)]]



def decompress(pixels):
    doubleColumn = duplicate(pixels)
    return list(map(lambda x:duplicate(x), doubleColumn))
def duplicate(l):
    if l == []:
        return []
    else:
        head = l[0]
        tail = l[1:]
        recursiveResult = duplicate(tail)
        return [head] + [head] + recursiveResult
def test_decompress():
    assert decompress([[pixel(r=10, g=23, b=52)],\
                       [pixel(r=40, g=68, b=92)]])==\
                       [[pixel(r=10, g=23, b=52), pixel(r=10, g=23, b=52)], \
                        [pixel(r=10, g=23, b=52), pixel(r=10, g=23, b=52)], \
                        [pixel(r=40, g=68, b=92), pixel(r=40, g=68, b=92)], \
                        [pixel(r=40, g=68, b=92), pixel(r=40, g=68, b=92)]]

        


# read the PPM image file named fname and convert it to a list of lists of pixels.
# each pixel is an RGB triple, represented using the type pixel defined above.
# each list of pixels represents one row in the image, ordered from top to bottom.
def readPPM(fname):
    f = open(fname, "rb")
    p6Ignore = f.readline()
    dimensions = f.readline().split()
    width = int(dimensions[0])
    height = int(dimensions[1])
    maxIgnore = f.readline()

    pixels = []
    rgbData = [x for x in f.read()]
    f.close()
    for r in range(height):
        row = []
        for c in range(width):
            i = 3 * (r * width + c)
            row.append(pixel(r=rgbData[i], g=rgbData[i+1], b=rgbData[i+2]))
        pixels.append(row)
    return pixels


# pixels should be a list of list of RGB triples, in the same format as returned
# by the readPPM function above.
# this function writes those pixels to the file named fname as a PPM image.
def writePPM(pixels, fname):
    f = open(fname, "wb")
    f.write("P6\n".encode())
    width = len(pixels[0])
    height = len(pixels)
    f.write((str(width) + " " + str(height) + "\n").encode())
    f.write((str(255) + "\n").encode())
    bPixels = [[struct.pack('BBB', p.r, p.g, p.b) for p in r] for r in pixels]
    flatPixels = reduce(lambda x,y: x+y, bPixels)
    f.writelines(flatPixels)
    f.close()
