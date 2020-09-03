import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .utilities import _coord_text

def image_text(text="Hello", width=500, height=500, x=0, y=0, size="auto", color="black", background="white", font="arial.ttf", blur=0, image=None, **kwargs):
    """
    Parameters
    ----------
    font : str
        The name of the font to be used. Note that the font is what controls features like bold / italic.
    For instance, 'arialbd.ttf', 'ariblk.ttf' or 'ariali.ttf' can be used for bold, black and italic, respectively.

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.image_text(text="Hello", size=40)  #doctest: +SKIP
    >>> image = ill.image_text(image=image, size=30, y=0.5, text="I'm Red", color="red")  #doctest: +SKIP
    >>> image = ill.image_text(image=image, size=20, x=0.5, text="Bold and blurred", font="arialbd.ttf", blur=0.005)  #doctest: +SKIP
    >>> image  #doctest: +SKIP
    >>> ill.image_text(text="3D", width=1600, height=900, font="arial.ttf", blur=0.01)  #doctest: +SKIP
    """
    # Get image
    if image is None:
        image  = PIL.Image.new('RGBA', (width, height), color = background)
    else:
        image = image.convert("RGBA")
    width, height = image.size

    # Create mask
    mask = PIL.Image.new('RGBA', (width, height))
    draw = PIL.ImageDraw.Draw(mask)

    # Get coordinates
    coord, font = _coord_text(mask, text=text, size=size, x=x, y=y, font=font)

    # Draw
    draw.text(coord, text, font=font, fill=color)

    # Blur the image a bit
    if blur > 0:
        mask = mask.filter(PIL.ImageFilter.GaussianBlur(blur * height))

    # Merge and return
    image = PIL.Image.alpha_composite(image, mask)

    return image
