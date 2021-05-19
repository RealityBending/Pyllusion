import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from .utilities import _coord_line


def image_line(
    width=800,
    height=600,
    x=0,
    y=0,
    x1=None,
    y1=None,
    x2=None,
    y2=None,
    length=1,
    rotate=0,
    size=1,
    color="black",
    background="white",
    blur=0,
    antialias=True,
    image=None,
    adjust_width=False,
    adjust_height=False,
    **kwargs
):
    """
    Creates a PIL image of a line.

    Parameters
    ----------
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    x : int
        x-coordinates of the center of the line, from -1 to 1.
    y : int
        y-coordinates of the center of the line, from -1 to 1.
    x1, x2 : int
        x-coordinates of the ends of the line, from -1 to 1. If not None, x is set to None.
    y1, y2 : int
        y-coordinates of the ends of the line, from -1 to 1. If not None, y is set to None.
    length : int
        Length of the line returned.
    rotate : float
        The orientation of the line in degrees, 0 being vertical and
        positive values rotating clockwise. Beyond 360 and below zero values wrap appropriately.
    size : int
        Width of the line returned.
    color : str
        Color of the line returned.
    background : str
        Background color.
    blur : int
        The degree of blur filter for the image returned.
    antialias : bool
        If true, resize the image using a high-quality downsampling filter.
    image : Image
        If None, an image will be created.
    adjust_width : bool
        If set to True and image is not None, the x-coordinates of the line can be adjusted
        to the height and width of the input image.
    adjust_height : bool
        If set to True and image is not None, the y-coordinates of the line can be adjusted
        to the height and width of the input image.

    Returns
    -------
    Image
        Image of a line.

    Examples
    --------
    >>> import pyllusion
    >>>
    >>> image = pyllusion.image_line(x=0, y=0, length=1)
    >>> image = pyllusion.image_line(image=image, x1=0, y1=0, length=0.5, rotate=90, color="green")
    >>> image = pyllusion.image_line(image=image, x1=0, y1=0, length=0.5, rotate=45)
    >>> image = pyllusion.image_line(image=image, x=0, y=0, length=1, rotate=135, color="blue")
    >>> image = pyllusion.image_line(image=image, length=1, rotate=20, color="red")
    >>> image = pyllusion.image_line(image=image, x1=0, y1=0, length=0.5, rotate=-90, size=3)
    >>> image = pyllusion.image_line(image=image, x1=-1, y1=-1, length=1, rotate=45, size=5, blur=0.005)
    >>> image
    """
    # Get image
    if image is None:
        image = PIL.Image.new("RGBA", (width, height), color=background)
    else:
        image = image.convert("RGBA")
    width, height = image.size

    # Upsample
    if antialias is True:
        width, height = width * 3, height * 3

    # Create mask
    mask = PIL.Image.new("RGBA", (width, height))
    draw = PIL.ImageDraw.Draw(mask)

    # Get coordinates
    coord, length, angle = _coord_line(
        mask,
        x=x,
        y=y,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        length=length,
        angle=rotate,
        adjust_width=adjust_width,
        adjust_height=adjust_height,
    )

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
