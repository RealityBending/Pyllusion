import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps


def image_text(text="Hello", width=500, height=500, color="black", background="white", font="arial.ttf"):
    """
    Parameters
    ----------
    font : str
        The name of the font to be used. Note that the font is what controls features like bold / italic.
    For instance, 'arialbd.ttf', 'arialblk.ttf' or 'ariali.ttf' can be used for bold, black and italic, respectively.

    Examples
    --------
    >>> import pyllusion as pyl
    >>>
    >>> pyl.image_text(text="Hello")
    >>> pyl.image_text(text="Hello", font="arialbd.ttf", color="red")
    """
    img  = PIL.Image.new('RGB', (width, height), color = background)
    draw = PIL.ImageDraw.Draw(img)

    # Initialize values
    size, text_width = 0, 0
    # Loop until max size is reached
    while text_width <= 0.9 * width:
        loaded_font = PIL.ImageFont.truetype(font, size)
        text_width, text_height = loaded_font.getsize(text)
        size += 1  # Increment text size

    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2

    # font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 36)
    draw.text((text_x, text_y), text, font=loaded_font, fill=color)
    return img
