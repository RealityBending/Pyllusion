import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps
import scipy.signal

from .rescale import rescale
from .utilities import _coord_circle


def image_blobs(width=500, height=500, n=100, sd=8, weight=1):
    """Return an image with blobs of the same standard deviations (SD).

    Parameters
    ----------
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    n : int
        Number of gaussian blobs drawn in the returned image.
    sd : int
        The standard deviation of the gaussian blob. Unit in pixel.
    weight : int
        A multiplication weight in case there are several layers of SDs.

    Returns
    -------
    Image
        Image of blob(s).

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> ill.image_blobs(n=500)  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>
    >>> ill.image_blobs(n=[5, 300, 1000], sd=[50, 10, 5])  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>

    """
    # Sanitize input
    if isinstance(sd, (int, float)):
        sd = [sd]
    if isinstance(n, (int, float)):
        n = [n]
    if isinstance(weight, (int, float)):
        weight = [weight]
    if len(n) != len(sd):
        raise TypeError("'n' must be of the same length as 'sd'.")
    if isinstance(width, tuple):
        height = width[1]
        width = width[0]

    # Add layers
    array = np.zeros((height, width))
    for i, current_sd in enumerate(sd):
        for _ in range(int(n[i])):
            x = np.random.randint(width)
            y = np.random.randint(height)
            blob = _image_blob(x=x, y=y, width=width, height=height, sd=int(current_sd))
            array += (blob * weight[i])

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






def _image_blob(x=400, y=300, width=800, height=600, sd=30):
    """Returns a 2D Gaussian kernel.

    >>> import pyllusion as ill
    >>> import matplotlib.pyplot as plt
    >>> array = _image_blob(sd=30)
    >>> plt.imshow(array)  #doctest: +ELLIPSIS
     <...>
    """
    parent_width = 3 * (np.max([x, y,  height - x, width - y]))
    gkern1d = scipy.signal.gaussian(parent_width, std=sd).reshape(parent_width, 1)
    parent_blob = np.outer(gkern1d, gkern1d)

    w = np.int(parent_width / 2)
    return parent_blob[w - y : (w - y) + height, w - x : (w - x) + width]




def _draw_blob(width, height=None, size=0.1, blur=0, color="black"):
    # Retrieve dimensions
    if height is None:
        width, height = width
    elif isinstance(width, PIL.Image.Image):
        width, height = width.size

    # Create mask of image size
    blob = PIL.Image.new("RGBA", (width, height))

    # Blob coordinates
    coord = _coord_circle(
        blob, diameter=size, x=np.random.uniform(-1, 1), y=np.random.uniform(-1, 1)
    )

    # Draw blob
    draw = PIL.ImageDraw.Draw(blob)
    draw.ellipse(coord, fill=color)

    blob = blob.filter(PIL.ImageFilter.GaussianBlur(radius=blur * 0.01 * width))
    return blob
