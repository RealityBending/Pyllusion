import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from .image import image_noise, image_text


# =============================================================================
# Autostereogram
# =============================================================================






def autostereogram(stimulus="Hello", pattern=None, n_repetitions=14, depth=1, invert=False, **kwargs):
    """
    Given a depth map, return an autostereogram Image computed from that depth
    map.

    Examples
    ---------
    >>> import pyllusion as pyl
    >>>
    >>> pyl.autostereogram(stimulus="3D", width=1000, height=500, font="arialbd.ttf")
    >>> pyl.autostereogram(stimulus="3D",
    ...                    pattern=pyllusion.random_circles,
    ...                    n_repetitions=20,
    ...                    n_circles=6000,
    ...                    invert=True,
    ...                    alpha=0.75,
    ...                    size_max=0.06)
    """
    # If '/' and '.' in string, we assume it's a path
    if "/" in stimulus and "." in stimulus:
        depth_map = PIL.Image.open(stimulus)
    else:  # Else a text
        depth_map = image_text(text=stimulus, **kwargs)

    # Convert to black and white
    depth_map = depth_map.convert('L')
    depth_map = PIL.ImageOps.autocontrast(depth_map)

    # Get size of depth map
    width, height = depth_map.size

    # We want the strip width to be a multiple of the tile
    # width so it repeats cleanly.
    strip_width = np.int(width / n_repetitions)

    image = PIL.Image.new("RGB", (width, height))

    # Create strip of pattern
    if pattern is None:
        strip = image_noise(width=strip_width, height=height, **kwargs)
    else:
        strip = pattern(width=strip_width, height=height, **kwargs)
    strip_pixels = strip.load()

    # Load pixels for easy replacement
    depth_pixels = depth_map.load()
    image_pixels = image.load()

    invert = -1 if invert else 1
    for x in range(width):
        for y in range(height):
            # Need one full strip's worth to borrow from.
            if x < strip_width:
                image_pixels[x, y] = strip_pixels[x, y]
            else:
                shift_amplitude = depth * (depth_pixels[x, y] / n_repetitions)
                shift_amplitude = invert * shift_amplitude
                image_pixels[x, y] = image_pixels[x - strip_width + shift_amplitude, y]

    # Add guide
    draw = PIL.ImageDraw.Draw(image)
    for i in [-2, 0]:
        diameter = 0.005 * width
        center_x = (width / 2) + (i * strip_width / 2)
        center_y = 0.5 * height
        draw.ellipse([center_x-diameter, center_y-diameter, center_x+diameter, center_y+diameter], fill=(255, 0, 0))
    return image