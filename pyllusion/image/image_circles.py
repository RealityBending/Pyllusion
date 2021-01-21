import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from .utilities import _color, _coord_circle

def image_circles(
    width=500,
    height=500,
    n=100,
    x=None,
    y=None,
    size_min=0.05,
    size_max=0.2,
    size=None,
    color=None,
    alpha=1,
    blur=0,
    antialias=True,
    image=None,
    background="white",
):
    """
    Creates a PIL image of circles.

    Parameters
    ----------
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    n : int
        Number of circles drawn in the returned image.
    x : Union[list, np.array, pd.Series]
        x-coordinates of all circles from -1 to 1.
    y : Union[list, np.array, pd.Series]
        y-coordinates of all circles from -1 to 1.
    size_min, size_max : int
        The minimum and maximum diameter of the circles drawn. Used only if size is None.
        If used, circles of random diameters from size_min to size_max are displayed.
    size : int
        The diameters of the circles drawn. Defaults to None.
    color : str
        Color of the circles returned.
    alpha : int
        Transparency of the circles drawn, 0 (transparent) to 1 (opaque).
    blur : int
        Degree of blur filter for the image returned.
    antialias : bool
        If true, resize the image using a high-quality downsampling filter.
    image : Image
        If None, an image will be created.
    background : str
        Color of the background.

    Returns
    -------
    Image
        Image of circle(s).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_circles()
    >>> image = ill.image_circles(color="bw", blur=0.01)
    >>> image = ill.image_circles(n=250, size_min=0.1, size_max=0.6, alpha=0.5)
    >>> image
    """
    # Sanity checks
    if size_max <= size_min:
        size_min = size_max / 10

    # Get image
    if image is None:
        image = PIL.Image.new("RGB", (width, height), color=background)

    # Sanitize circle parameters
    if x is None:
        x = np.random.uniform(-1, 1, n)
    if y is None:
        y = np.random.uniform(-1, 1, n)
    if size is None:
        size = np.random.uniform(size_min, size_max, n)
    else:
        try:
            len(size)
        except TypeError:
            size = [size] * n
    if color is None:
        color = np.random.randint(0, 256, size=(n, 3))
    elif isinstance(color, str):
        if color in ["bw", "blackwhite"]:
            color = np.random.randint(0, 256, size=n)
        else:
            color = [color] * n

    # Draw circle
    for i in range(n):
        # Draw
        image = image_circle(
            image=image,
            x=x[i],
            y=y[i],
            size=size[i],
            color=color[i],
            alpha=alpha,
            blur=blur,
            antialias=antialias,
        )

    return image


def image_circle(
    width=800,
    height=600,
    x=0,
    y=0,
    size=1,
    color="black",
    outline=0,
    color_outline="black",
    alpha=1,
    blur=0,
    antialias=True,
    image=None,
    background="white",
):
    """
    Creates a PIL image of a circle.

    Parameters
    ----------
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    x : Union[list, np.array, pd.Series]
        x-coordinates of the circle from -1 to 1.
    y : Union[list, np.array, pd.Series]
        y-coordinates of the circle from -1 to 1.
    size : int
        The diameter of the circle drawn.
    color : str
        Color of the circle returned.
    outline : float
        The width of the outline of the circle.
    color_outline : str
        Outline of the circle outline returned.
    alpha : int
        Transparency of the circle drawn, 0 (transparent) to 1 (opaque).
    blur : int
        Degree of blur filter for the image returned.
    antialias : bool
        If true, resize the image using a high-quality downsampling filter.
    image : Image
        If None, an image will be created.
    background : str
        Color of the background.

    Returns
    -------
    Image
        Image of circle.

    Examples
    --------
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

    # Circle coordinates
    coord = _coord_circle(mask, diameter=size, x=x, y=y)

    # Draw circle
    draw.ellipse(
        coord,
        fill=tuple(_color(color, alpha=alpha, mode="RGBA")),
        width=outline,
        outline=color_outline,
    )

    # resize with antialiasing
    if antialias is True:
        mask = mask.resize(image.size, PIL.Image.ANTIALIAS)

    # Blur the image a bit
    if blur > 0:
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(blur * mask.size[1]))

    # Merge and return
    image = PIL.Image.alpha_composite(image, mask)
    return image
