import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps


def image_scramble(image, blocks=(10, 10)):
    """
    Scramble an image.

    Parameters
    ----------
    image : PIL.Image
        Image to scramble.
    blocks : tuple
        Minimum number of blocks in the x and y direction. Might be higher if the
        image is not divisible by the number of blocks.

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

    """
    n_blocks_width = _find_best_divisor(image.width, blocks[0], blocks[0] * 2)
    n_blocks_height = _find_best_divisor(image.height, blocks[1], blocks[1] * 2)

    array = np.array(image)
    horizontal = np.array_split(array, n_blocks_width)
    np.random.shuffle(horizontal)  # Shuffle (in-place)
    vertical = [
        _return_shuffled(np.array_split(block, n_blocks_height, axis=1)) for block in horizontal
    ]

    array = np.concatenate(np.concatenate(vertical, axis=1), axis=1)
    return PIL.Image.fromarray(array)


def _return_shuffled(x):
    """Return a shuffled array. Because python does it in-place."""
    np.random.shuffle(x)
    return x


def _find_best_divisor(number, low, high, step=1):
    """Return the closest divisor so that the remainder is 0"""
    minimal_truncation, best_divisor = min(
        (number % divisor, divisor) for divisor in range(low, high, step)
    )
    if minimal_truncation != 0:
        raise ValueError("No divisor found. Please increase the number of blocks.")
    return best_divisor
