import numpy as np
import scipy.signal
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .utilities import _coord_circle
from .rescale import rescale

def image_blobs(width=500, height=500, n=100, sd=8):
    """Return an image with blobs of the same standard deviations (SD).

    >>> import pyllusion as ill
    >>>
    >>> ill.image_blobs(n=500)  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>

    """

    array = np.zeros((height, width))
    for _ in range(n):
        x = np.random.randint(width)
        y = np.random.randint(height)
        blob = _image_blob(x=x, y=y, width=width, height=height, sd=sd)
        array += blob

    array = rescale(array, to=[0, 255])
    image = PIL.Image.fromarray(array.astype(np.uint8))
    return image


def image_blob(x=450, y=100, width=800, height=600, sd=3):
    """Return an image of blob
    """
    array = _image_blob(x=x, y=y, width=width, height=height, sd=sd)
    array = rescale(array, to=[0, 255])
    image = PIL.Image.fromarray(array.astype(np.uint8))
    return image


def _image_blob(x=450, y=100, width=800, height=600, sd=3):
    """Returns a 2D Gaussian kernel.

    >>> import pyllusion as ill
    >>> import matplotlib.pyplot as plt
    >>> array = _image_blob(sd=8)
    >>> plt.imshow(array)  #doctest: +ELLIPSIS
     <...>
    """

    _x = height - x
    _y = width - y
    parent_width = 3 * (np.max([x, y, _x, _y]))
    gkern1d = scipy.signal.gaussian(parent_width, std=sd).reshape(parent_width, 1)
    parent_blob = np.outer(gkern1d, gkern1d)

    w = int(parent_width / 2)
    blob = parent_blob[w - y: (w - y) + height, w - x: (w - x) + width]
    return blob


def _draw_blob(width, height=None, size=0.1, blur=0, color="black"):
    # Retrieve dimensions
    if height is None:
        width, height = width
    elif isinstance(width, PIL.Image.Image):
        width, height = width.size

    # Create mask of image size
    blob = PIL.Image.new("RGBA", (width, height))

    # Blob coordinates
    coord = _coord_circle(blob,
                            diameter=size,
                            x=np.random.uniform(-1, 1),
                            y=np.random.uniform(-1, 1))

    # Draw blob
    draw = PIL.ImageDraw.Draw(blob)
    draw.ellipse(coord, fill=color)

    blob = blob.filter(PIL.ImageFilter.GaussianBlur(radius=blur * 0.01 * width))
    return blob
