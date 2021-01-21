import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from .utilities import _coord_text


def image_text(
    text="Hello",
    width=500,
    height=500,
    x=0,
    y=0,
    size="auto",
    color="black",
    background="white",
    font="arial.ttf",
    blur=0,
    image=None,
):
    """
    Creates a PIL image of text.


    Parameters
    ----------
    text : str
        The text displayed in the image returned.
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    x : int
        x-coordinates of the center of the text display, from -1 to 1.
    y : int
        y-coordinates of the center of the text display, from -1 to 1.
    size : int
        Requested size, in points, for the text. If "auto", the maximum size that
        fits the image will be chosen.
    color : str
        Text color.
    background : str
        Background color.
    font : str
        The name of the font to be used. Note that the font is what controls features like
        bold / italic. For instance, 'arialbd.ttf', 'ariblk.ttf' or 'ariali.ttf' can be
        used for bold, black and italic, respectively.
    blur : int
        The degree of blur filter for the image returned.
    image : Image
        If None, an image will be created.

    Returns
    -------
    Image
        Image of a text.

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_text(text="Hello", size=40)
    >>> image = ill.image_text(image=image, size=30, y=0.5, text="I'm Red", color="red")
    >>> image = ill.image_text(image=image, size=20, x=0.5, text="Bold and blurred", font="arialbd.ttf", blur=0.005)
    >>> image
    >>> ill.image_text(text="3D", width=1600, height=900, font="arial.ttf", blur=0.01)
    >>> image
    """
    # Get image
    if image is None:
        image = PIL.Image.new("RGBA", (width, height), color=background)
    else:
        image = image.convert("RGBA")
    width, height = image.size

    # Create mask
    mask = PIL.Image.new("RGBA", (width, height))
    draw = PIL.ImageDraw.Draw(mask)

    # Get coordinates
    coord, font, _, _ = _coord_text(mask, text=text, size=size, x=x, y=y, font=font)

    # Draw
    draw.text(coord, text, font=font, fill=color)

    # Blur the image a bit
    if blur > 0:
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(blur * height))

    # Merge and return
    image = PIL.Image.alpha_composite(image, mask)

    return image
