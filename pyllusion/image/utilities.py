import numpy as np

from .rescale import rescale




def _rgb(x):
    """Convert 0-1 values to RGB 0-255 values.
    """
    return rescale(x, to=[0, 255], scale=[0, 1])



def _coord_circle(image, diameter=0.1, x=0, y=0, unit="grid"):
    """Get circle coordinates

    Examples
    --------
    >>> import pyllusion as pyl
    >>>
    >>> image  = PIL.Image.new('RGB', (500, 400), color = "white")
    >>> draw = PIL.ImageDraw.Draw(image, 'RGBA')
    >>>
    >>> coord = _coord_circle(image, diameter=1, x=0, y=0)
    >>> draw.ellipse(coord, fill="red", width=0)
    >>> draw.ellipse(_coord_circle(image, diameter=1.5, x=0, y=0), outline="blue")
    >>> image
    """
    if unit == "grid":
        # Get coordinates in pixels
        width, height = image.size
        x = np.int(rescale(x, to=[0, width], scale=[-1, 1]))
        y = np.int(rescale(y, to=[0, height], scale=[-1, 1]))

        # Convert diameter based on width
        diameter = np.int(rescale(diameter, to=[0, width], scale=[0, 2]))
        diameter = 2 if diameter < 2 else diameter

    radius = diameter / 2
    # Choose diameter and centre
    coord = [(x-radius, y-radius), (x+radius, y+radius)]

    return coord