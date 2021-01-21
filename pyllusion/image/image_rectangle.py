import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from .utilities import _color, _coord_rectangle


def image_rectangle(
    width=800,
    height=600,
    x=0,
    y=0,
    size_width=1,
    size_height=1,
    rotate=0,
    color="black",
    outline=0,
    color_outline="black",
    background="white",
    alpha=1,
    blur=0,
    antialias=True,
    adjust_width=False,
    adjust_height=False,
    image=None,
):
    """
    Creates a PIL image of a rectangle.

    Parameters
    ----------
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    x : Union[list, np.array, pd.Series]
        x-coordinates of the rectangle from -1 to 1.
    y : Union[list, np.array, pd.Series]
        y-coordinates of the rectangle from -1 to 1.
    size_width : int
        Width of the rectangle drawn.
    size_height : int
        Height of the rectangle drawn.
    rotate : int
        The orientation of the rectangle in degrees, 0 being vertical and
        positive values rotating clockwise.
    color : str
        Color of the line returned.
    outline : int
        Width of the outline.
    color_outline : str
        Color of the outline.
    background : str
        Color of the background.
    alpha : int
        Transparency of the rectangle drawn, 0 (transparent) to 1 (opaque).
    blur : int
        Degree of blur filter for the image returned.
    antialias : bool
        If true, resize the image using a high-quality downsampling filter.
    adjust_width : bool
        If set to True, the size_width can be adjusted to the height and width of the
        image.
    adjust_height : bool
        If set to True, the size_height can be adjusted to the height and width of the
        image.
    image : Image
        If None, an image will be created.    

    Returns
    -------
    Image
        Image of a rectangle.

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_rectangle(x=0, y=0, color=(0,0,0,0), outline=3, rotate=1)
    >>> image = ill.image_rectangle(image=image, x=0.5, size_width=0.5, rotate=45, color="red")
    >>> image = ill.image_rectangle(image=image, y=0.25, size_height=0.2,  color="yellow", alpha=0.5)
    >>> image = ill.image_rectangle(image=image, size_width=0.5, size_height=0.5, blur=0.01, color="green", adjust_width=True)
    >>> image
    """
    # Get image
    if image is None:
        image = PIL.Image.new("RGBA", (width, height), color=background)
    else:
        image = image.convert("RGBA")
    width, height = image.size

    # Adjust size for screen ratio
    if adjust_width is True:
        size_width = size_width * (height / width)
    if adjust_height is True:
        size_height = size_height * (width / height)

    # Upsample
    if antialias is True:
        width, height = width * 3, height * 3

    # Create mask
    mask = PIL.Image.new("RGBA", (width, height))
    draw = PIL.ImageDraw.Draw(mask)

    # Get coordinates
    coord = _coord_rectangle(
        mask, x=x, y=y, size_width=size_width, size_height=size_height
    )

    # Draw
    draw.rectangle(
        coord,
        fill=_color(color, alpha=alpha, mode="RGBA"),
        width=outline,
        outline=color_outline,
    )

    # Rotate
    if rotate != 0:
        mask = mask.rotate(-rotate)

    # resize with antialiasing
    if antialias is True:
        mask = mask.resize(image.size, PIL.Image.ANTIALIAS)

    # Blur the image a bit
    if blur > 0:
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(blur * height))

    # Merge and return
    image = PIL.Image.alpha_composite(image, mask)

    return image
