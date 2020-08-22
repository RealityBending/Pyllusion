import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
import numpy as np
from .utilities import _coord_line


def image_line(width=800, height=600, x=0, y=0, x2=None, y2=None, length=1, angle=0, size=1, color="black", background="white", blur=0, antialias=True, image=None, **kwargs):
    """
    Parameters
    ----------

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_line(x=0, y=0, length=0.5, angle=90)
    >>> image = ill.image_line(image=image, x=0, y=-0.5, length=1, angle=0, color="red")
    >>> image = ill.image_line(image=image, x=0, y=0, length=0.5, angle=-90, size=3)
    >>> image = ill.image_line(image=image, x=-1, y=-1, length=1, angle=45, size=5, blur=0.01)
    >>> image
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
    # coord = _coord_line(mask, text=text, size=size, x=x, y=y, font=font)
    coord, length, angle = _coord_line(mask, x1=x, y1=y, x2=x2, y2=y2, length=length, angle=angle)

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

