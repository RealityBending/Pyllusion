import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .utilities import _rgb


def image_noise(width=500, height=500, red=np.random.uniform,
                 green=np.random.uniform, blue=np.random.uniform,
                 blackwhite=False, blur=0, **kwargs):
    """
    Generate an RGB Image of specific dimensions made of random dots.

    Examples
    ----------
    >>> import pyllusion as ill
    >>>
    >>> ill.image_noise()  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>
    >>> ill.image_noise(blackwhite=True)  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>
    >>> ill.image_noise(blur=0.005)  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>
    """
    # Generate random colors
    r = red(size=(width, height), **kwargs)
    g = green(size=(width, height), **kwargs)
    b = blue(size=(width, height), **kwargs)

    pixels = np.array([_rgb(r), _rgb(g), _rgb(b)]).T

    # Convert to PIL image
    image = PIL.Image.fromarray(pixels.astype('uint8'), 'RGB')

    # Convert to black and white
    if blackwhite is True:
        image = image.convert('L').convert('RGB')

    # Blur the background a bit
    if blur > 0:
        image = image.filter(PIL.ImageFilter.GaussianBlur(blur * height))

    return image
