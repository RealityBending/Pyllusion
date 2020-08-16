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
    >>> import pyllusion as pyl
    >>>
    >>> pyl.image_noise(width=300, height=300)
    >>> pyl.image_noise(width=300, height=300, blackwhite=True)
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
    image = image.filter(PIL.ImageFilter.BoxBlur(blur * 0.01 * np.min([width, height])))

    return image
