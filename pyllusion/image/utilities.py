import numpy as np
import PIL.ImageColor

from .rescale import rescale






def _rgb(x):
    """Convert 0-1 values to RGB 0-255 values.
    """
    return rescale(x, to=[0, 255], scale=[0, 1])


def _color(color="black", alpha=1, mode="RGB"):
    """Sanitize color to RGB(A) format.
    """
    if isinstance(color, str):
        color = PIL.ImageColor.getrgb(color)

    # Add transparency
    if mode == "RGBA":
        if len(color) == 3:
            color = color + tuple([np.int(_rgb(alpha))])

    return color


def _coord_circle(image, diameter=0.1, x=0, y=0, unit="grid"):
    """Get circle coordinates

    Examples
    --------
    >>> import pyllusion as ill
    >>> import PIL.Image, PIL.ImageDraw
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
        y = np.int(rescale(-y, to=[0, height], scale=[-1, 1]))

        # Convert diameter based on height
        diameter = np.int(rescale(diameter, to=[0, height], scale=[0, 2]))
        diameter = 2 if diameter < 2 else diameter

    radius = diameter / 2
    # Choose diameter and centre
    coord = [(x-radius, y-radius), (x+radius, y+radius)]

    return coord


def _coord_text(image, text="hello", size="auto", x=0, y=0, font="arial.ttf", unit="grid"):
    """Get text coordinates

    Examples
    --------
    >>> import pyllusion as ill
    >>> import PIL.Image, PIL.ImageDraw
    >>>
    >>> image  = PIL.Image.new('RGB', (500, 500), color = "white")
    >>> draw = PIL.ImageDraw.Draw(image, 'RGB')
    >>>
    >>> coord, font = _coord_text(image, size="auto", x=-0.5, y=0.5)
    >>> draw.text(coord, text, fill="black", font=font)
    >>> image
    """
    if unit == "grid":
        # Get coordinates in pixels
        width, height = image.size
        x = np.int(rescale(x, to=[0, width], scale=[-1, 1]))
        y = np.int(rescale(-y, to=[0, height], scale=[-1, 1]))

    if size == "auto":
        # Initialize values
        size, top_left_x, top_left_y, right_x, bottom_y = 0, width, height, 0, 0
        # Loop until max size is reached
        while top_left_x > 0.01 * width and right_x < 0.99 * width and top_left_y > 0.01 * height and bottom_y < 0.99 * height:
            loaded_font = PIL.ImageFont.truetype(font, size)
            text_width, text_height = loaded_font.getsize(text)
            top_left_x = x - (text_width / 2)
            top_left_y = y - (text_height / 2)
            right_x = top_left_x + text_width
            bottom_y = top_left_y + text_height
            size += 1  # Increment text size
    else:
        loaded_font = PIL.ImageFont.truetype(font, size)
        text_width, text_height = loaded_font.getsize(text)
        top_left_x = x - (text_width / 2)
        top_left_y = y - (text_height / 2)

    coord = top_left_x, top_left_y

    return coord, loaded_font



def _coord_line(image=None, x1=0, y1=0, x2=None, y2=None, length=None, angle=None):
    if x2 is None and y2 is None:
        x2 = x1 + np.sin(np.deg2rad(angle)) * length
        y2 = y1 + np.cos(np.deg2rad(angle)) * length
    if length is None and angle is None:
        length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        angle = np.rad2deg(np.arccos(np.abs(x1-x2) / length))

    # Get coordinates in pixels
    if image is not None:
        width, height = image.size
        x1 = np.int(rescale(x1, to=[0, width], scale=[-1, 1]))
        y1 = np.int(rescale(-y1, to=[0, height], scale=[-1, 1]))
        x2 = np.int(rescale(x2, to=[0, width], scale=[-1, 1]))
        y2 = np.int(rescale(-y2, to=[0, height], scale=[-1, 1]))
        length = np.int(rescale(length, to=[0, height], scale=[0, 2]))
    return (x1, y1, x2, y2), length, angle
