import numpy as np
import scipy.signal
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .utilities import _coord_circle

def image_blobs(width=500, height=500, n=100,
                size=0.1, blur=0.1, color="black", background="white"):
    """
    >>> import pyllusion as pyl
    >>>
    >>> pyl.image_blobs(width=480, blur=1, size=0.1)
    """

    # Create white canvas and get drawing context
    image  = PIL.Image.new('RGBA', (width, height), color = background)

    for _ in range(n):
        # Create mask of image size
        blob = _draw_blob(image.size, size=size, blur=blur, color=color)
        image = PIL.Image.alpha_composite(image, blob)

    return image.convert("RGB")


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






def _gaussian_kernel(x=280, y=280, width=480, sd=3):
    """Returns a 2D Gaussian kernel.

    >>> array = _gaussian_kernel(width=480, sd=8)
    >>> array = pyl.rescale(array, scale=[0, 1], to=[0, 255])
    >>> PIL.Image.fromarray(array.astype(np.uint8))
    """

    width_blob = sd * 8
    gkern1d = scipy.signal.gaussian(width_blob, std=sd).reshape(width_blob, 1)
    blob = np.outer(gkern1d, gkern1d)

    image = np.zeros((width, width))
    image[x: x + width_blob, y: y + width_blob] += blob
    return image


