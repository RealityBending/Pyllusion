import numpy as np
from .image import image_blobs
from .image import rescale
import PIL.Image


def pareidolia(width=480, height=480):
    """
    >>> import pyllusion as pyl
    >>>
    >>> pyl.pareidolia(width=480, height=480, blur=blur_64, size=size, background="black", color="white")
    """
    blur_modifier = 1.3

    blur_64 = blur_modifier * (10 * 64 / width)
    blur_64 = image_blobs(width=width, height=height, blur=blur_64, size=0.1, n=2500, background="black", color="white")

    blur_256 = blur_modifier * (10 * 256 / width)
    blur_256 = image_blobs(width=width, height=height, blur=blur_256, size=0.3, n=156, background="black", color="white")

    blur_1024 = blur_modifier * (10 * 1024 / width)
    blur_1024 = image_blobs(width=width, height=height, blur=blur_1024, size=0.8, n=10, background="black", color="white")

    array = np.array(blur_64) + 5.0*np.array(blur_256) + 25.0*np.array(blur_1024)
    array = rescale(array, to=[0, 255])
    image = PIL.Image.fromarray(array.astype(np.uint8))

    return image