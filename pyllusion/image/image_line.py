import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
import numpy as np
from .utilities import _coord_line


def image_line(width=800, height=600, x=0, y=0, x1=None, y1=None, x2=None, y2=None, length=1, rotate=0, size=1, color="black", background="white", blur=0, antialias=True, image=None, adjust_width=False, adjust_height=False, **kwargs):
    """
    Parameters
    ----------

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_line(x=0, y=0, length=1)
    >>> image = ill.image_line(image=image, x1=0, y1=0, length=0.5, rotate=90, color="green")
    >>> image = ill.image_line(image=image, x1=0, y1=0, length=0.5, rotate=45)
    >>> image = ill.image_line(image=image, x=0, y=0, length=1, rotate=135, color="blue")
    >>> image = ill.image_line(image=image, length=1, rotate=20, color="red")
    >>> image = ill.image_line(image=image, x1=0, y1=0, length=0.5, rotate=-90, size=3)
    >>> image = ill.image_line(image=image, x1=-1, y1=-1, length=1, rotate=45, size=5, blur=0.005)
    >>> image  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>
    """
    # Get image
    if image is None:
        image  = PIL.Image.new('RGBA', (width, height), color = background)
    else:
        image = image.convert("RGBA")
    width, height = image.size

    # Upsample
    if antialias is True:
        width, height = width * 3, height * 3

    # Create mask
    mask = PIL.Image.new('RGBA', (width, height))
    draw = PIL.ImageDraw.Draw(mask)

    # Get coordinates
    coord, length, angle = _coord_line(mask, x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2, length=length, angle=rotate, adjust_width=adjust_width, adjust_height=adjust_height)

    # Draw
    draw.line(coord, fill=color, width=size)

    # resize with antialiasing
    if antialias is True:
        mask = mask.resize(image.size, PIL.Image.ANTIALIAS)

    # Blur the image a bit
    if blur > 0:
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(blur * height))

    # Merge and return
    image = PIL.Image.alpha_composite(image, mask)

    return image

