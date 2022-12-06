import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps


def image_scramble(image, blocks=None, omit=None):
    """
    Scramble an image.

    .. note ::

        We would like to implement diffeomorphic scrambling by translating this matlab code
        https://github.com/rhodricusack/diffeomorph/blob/master/diffeomorphic.m
        Consider helping us!
        See also: https://jov.arvojournals.org/article.aspx?articleid=2193914

    Parameters
    ----------
    image : PIL.Image
        Image to scramble.
    blocks : tuple
        Scramble with blocks. Minimum number of blocks in the x and y direction. Might be higher if
        the image is not divisible by the number of blocks. If ``None``, will scramble
        the pixels.
    omit : str
        If ``"white"`` or ``"black"``, will scramble all pixels but the totally white or black
        ones. Note that the ``blocks`` parameter will be ignored.

    Returns
    -------
    Image
        Scrambled image.

    Examples
    ----------
    >>> import pyllusion as ill
    >>>
    >>> image = ill.Ebbinghaus().to_image()
    >>> ill.image_scramble(image, blocks=(10, 10))
    >>> ill.image_scramble(image, blocks=(100, 100))
    >>> ill.image_scramble(image, blocks=None)
    >>> ill.image_scramble(image, omit="white")
    >>> ill.image_scramble(image, omit="black")

    """
    # If using a mask, do bespoke operation
    if omit is not None:
        return _scramble_with_mask(image, omit=omit)

    array = np.array(image)

    if blocks is None:
        array = _shuffled(_shuffled(array.swapaxes(0, 1)).swapaxes(0, 1))
        return PIL.Image.fromarray(array)

    n_blocks_width = _find_best_divisor(image.width, blocks[0], blocks[0] * 2)
    n_blocks_height = _find_best_divisor(image.height, blocks[1], blocks[1] * 2)

    horizontal = np.array_split(array, n_blocks_width)
    horizontal = _shuffled(horizontal)  # Shuffle (in-place)
    vertical = [_shuffled(np.array_split(block, n_blocks_height, axis=1)) for block in horizontal]

    array = np.concatenate(np.concatenate(vertical, axis=1), axis=1)
    return PIL.Image.fromarray(array)


def _scramble_with_mask(image, omit="white"):
    # https://stackoverflow.com/questions/74541109/
    array = np.array(image.convert("RGB"))  # Forge to RGB to have only 3 dimensions

    # Get mask of non-white or non-black pixels
    if omit == "white":
        mask = np.array(image.convert("L")) != 255
    elif omit == "black":
        mask = np.array(image.convert("L")) != 0
    else:
        raise ValueError("omit must be either 'white' or 'black'")

    # Make a single 24-bit number for each pixel, instead of 3x 8-bit numbers
    u32 = np.dot(array.astype(np.uint32), [1, 256, 65536])
    u32[mask] = _shuffled(u32[mask])

    # Now split 24-bit entities back into RGB888
    r = u32 & 0xFF
    g = (u32 >> 8) & 0xFF
    b = (u32 >> 16) & 0xFF
    array = np.dstack((r, g, b)).astype(np.uint8)
    return PIL.Image.fromarray(array)


# Internals
# ---------
def _shuffled(x):
    """Return a shuffled array. Because python does it in-place."""
    np.random.shuffle(x)
    return x


def _find_best_divisor(number, low, high, step=1):
    """Return the closest divisor so that the remainder is 0"""
    minimal_truncation, best_divisor = min(
        (number % divisor, divisor) for divisor in range(low, high, step)
    )
    if minimal_truncation != 0:
        raise ValueError(
            "No divisor found. Please increase the number of blocks"
            + f" (best in to input a number that is a divider of {number})."
        )
    return best_divisor
