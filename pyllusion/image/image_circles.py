import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .utilities import _rgb, _coord_circle


def image_circles(width=500, height=500, n=100,
                  size_min=0.01, size_max=0.25, size=None,
                  blackwhite=False, blur=0, alpha=1, background="white"):
    """
    >>> import pyllusion as pyl
    >>>
    >>> pyl.image_circles()
    >>> pyl.image_circles(blackwhite=True)
    >>> pyl.image_circles(n=200, alpha=0.5, blur=0.1)
    """
    # Create white canvas and get drawing context
    image  = PIL.Image.new('RGB', (width, height), color = background)
    draw = PIL.ImageDraw.Draw(image, 'RGBA')

    # Convert alpha value to 0-255 scale
    alpha = np.int(_rgb(alpha))

    # Draw circle
    for _ in range(n):
        # Choose RGB values for this circle
        rgb = tuple(np.random.randint(0, 256, size=3))
        # Diameter
        if size is not None:
            diameter = size
        else:
            diameter = np.random.uniform(size_min, size_max)
        # Circle coordinates
        coord = _coord_circle(image,
                              diameter=diameter,
                              x=np.random.uniform(-1, 1),
                              y=np.random.uniform(-1, 1))
        # Draw
        draw.ellipse(coord, fill=rgb + tuple([alpha]))

    # Convert to black and white
    if blackwhite is True:
        image = image.convert('L').convert('RGB')

    # Blur the background a bit
    image = image.filter(PIL.ImageFilter.BoxBlur(blur * 0.01 * width))

    return image