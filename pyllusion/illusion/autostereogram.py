import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_noise, image_text



def autostereogram(stimulus="Hello", pattern=None, n_repetitions=14, depth=1, invert=False, guide=True, **kwargs):
    """
    Given a depth map, return an autostereogram Image computed from that depth
    map.

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> ill.autostereogram(stimulus="3D", width=1000, height=500, font="arialbd.ttf")  #doctest: +SKIP
    >>> ill.autostereogram(stimulus="3D",
    ...                    pattern=ill.image_circles,
    ...                    n_repetitions=16,
    ...                    n=1000,
    ...                    invert=False,
    ...                    alpha=0.75,
    ...                    size_max=0.7)  #doctest: +SKIP
    """
    # If '/' and '.' in string, we assume it's a path
    if "/" in stimulus and "." in stimulus:
        depth_map = PIL.Image.open(stimulus)
    else:  # Else a text
        depth_map = image_text(text=stimulus, **kwargs)

    # Convert to black and white
    depth_map = depth_map.convert('L')
    depth_map = PIL.ImageOps.autocontrast(depth_map)

    if invert is False:
        depth_map = PIL.ImageOps.invert(depth_map)

    # Get size of depth map
    width, height = depth_map.size

    # We want the strip width to be a multiple of the tile
    # width so it repeats cleanly.
    strip_width = np.int(width / n_repetitions)

    image = PIL.Image.new("RGB", (width, height))

    # Fix conflicting arguments
    conflicting_args = ["width", "height", "font"]
    kwargs = {key: kwargs[key] for key in kwargs if key not in conflicting_args}

    # Create strip of pattern
    if pattern is None:
        strip = image_noise(width=strip_width, height=height, **kwargs)
    else:
        strip = pattern(width=strip_width, height=height, **kwargs)
    strip_pixels = strip.load()

    # Load pixels for easy replacement
    depth_pixels = depth_map.load()
    image_pixels = image.load()

    for x in range(width):
        for y in range(height):
            # Need one full strip's worth to borrow from.
            if x < strip_width:
                image_pixels[x, y] = strip_pixels[x, y]
            else:
                shift_amplitude = depth * (depth_pixels[x, y] / n_repetitions)
                image_pixels[x, y] = image_pixels[x - strip_width + shift_amplitude, y]

    # Add guide
    if guide is True:
        draw = PIL.ImageDraw.Draw(image)
        for i in [-2, 0]:
            diameter = 0.005 * width
            center_x = (width / 2) + (i * strip_width / 2)
            center_y = 0.5 * height
            draw.ellipse([center_x-diameter, center_y-diameter, center_x+diameter, center_y+diameter], fill=(255, 0, 0))
    return image
