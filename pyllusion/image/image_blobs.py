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
    >>> ill.image_blobs(n=100)  #doctest: +ELLIPSIS
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
        x = np.random.randint(width, size=n)
        y = np.random.randint(height, size=n)
        for j in range(int(n[i])):
            parent_blob = _image_blob_parent(x=x[j], y=y[j], width=width, height=height, sd=int(current_sd))
            blob = _image_blob_crop(parent_blob, x=x[j], y=y[j], width=width, height=height)
            array += (blob * weight[i])

    array = rescale(array, to=[0, 255])
    image = PIL.Image.fromarray(array.astype(np.uint8))
    return image












def image_blob(x=450, y=100, width=800, height=600, sd=3):
    """Return an image of blob
    """
    parent_blob = _image_blob_parent(x=x, y=y, width=width, height=height, sd=sd)
    blob = _image_blob_crop(parent_blob, x=x, y=y, width=width, height=height)
    blob = rescale(blob, to=[0, 255])
    image = PIL.Image.fromarray(blob.astype(np.uint8))
    return image






def _image_blob_crop(parent_blob, x=400, y=300, width=800, height=600):
    """Returns a 2D Gaussian kernel.

    >>> import matplotlib.pyplot as plt
    >>> parent_blob = _image_blob_parent(x=400, y=500, width=800, height=600, sd=30)
    >>> blob = _image_blob_crop(parent_blob, x=400, y=500, width=800, height=600)
    >>> plt.imshow(blob)  #doctest: +ELLIPSIS
     <...>
    """
    w = np.int(len(parent_blob) / 2)
    return parent_blob[w - y : (w - y) + height, w - x : (w - x) + width]


def _image_blob_parent(x=400, y=300, width=800, height=600, sd=30):
    """
    >>> import matplotlib.pyplot as plt
    >>> plt.imshow(_image_blob_parent(sd=30))  #doctest: +ELLIPSIS
     <...>
    """
    parent_width = 3 * (np.max([x, y,  height - x, width - y]))
    gkern1d = scipy.signal.gaussian(parent_width, std=sd).reshape(parent_width, 1)
    return np.outer(gkern1d, gkern1d)



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
