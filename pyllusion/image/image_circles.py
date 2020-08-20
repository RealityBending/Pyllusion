import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .utilities import _color, _rgb, _coord_circle
from .rescale import rescale


def image_circles(width=500, height=500, n=100,
                  size_min=0.05, size_max=0.2, size=None,
                  blackwhite=False, alpha=1, blur=0, antialias=True, image=None, background="white"):
    """
    >>> import pyllusion as ill
    >>>
    >>> ill.image_circles()
    >>> ill.image_circles(blackwhite=True, blur=0.01)
    >>> ill.image_circles(n=250, size_min=0.1, size_max=0.6, alpha=0.5)
    """
    # Sanity checks
    if size_max <= size_min:
        size_min = size_max / 10

    # Get image
    if image is None:
        image  = PIL.Image.new('RGB', (width, height), color = background)

    # Draw circle
    for _ in range(n):
        # Choose RGB values for this circle
        rgb = tuple(np.random.randint(0, 256, size=3))

        # Diameter
        if size is not None:
            diameter = size
        else:
            diameter = np.random.uniform(size_min, size_max)
        # Circle position
        x=np.random.uniform(-1, 1)
        y=np.random.uniform(-1, 1)

        # Draw
        image = image_circle(image=image, x=x, y=y, size=diameter, color=rgb, alpha=alpha, blur=blur, antialias=antialias)

    # Convert to black and white
    if blackwhite is True:
        image = image.convert('L').convert('RGB')

    return image




def image_circle(width=800, height=600, x=0, y=0, size=1, color="black", outline=0, color_outline="black", alpha=1, blur=0, antialias=True, image=None, background="white"):
    """
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_circle()
    >>> image = ill.image_circle(image=image, color="red", x=0.5, size=0.5)
    >>> image = ill.image_circle(image=image, color="blue", x=-0.3, size=0.5, blur=0.05)
    >>> image = ill.image_circle(image=image, color="yellow", y=0.5, alpha=0.5)
    >>> image = ill.image_circle(image=image, color="white", size=0.3, y=-0.5, outline=1)
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

    # Circle coordinates
    coord = _coord_circle(mask, diameter=size, x=x, y=y)

    # Draw circle
    draw.ellipse(coord, fill=_color(color, alpha=alpha, mode="RGBA"), width=outline, outline=color_outline)

    # resize with antialiasing
    if antialias is True:
        mask = mask.resize(image.size, PIL.Image.ANTIALIAS)

    # Blur the image a bit
    if blur > 0:
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(blur * mask.size[1]))

    # Merge and return
    image = PIL.Image.alpha_composite(image, mask)
    return image
