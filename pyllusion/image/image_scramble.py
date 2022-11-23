import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps


def image_scramble(image, blocks=(10, 10)):
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
        Minimum number of blocks in the x and y direction. Might be higher if the
        image is not divisible by the number of blocks. If ``None``, will scramble
        the pixels.

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

    """
    array = np.array(image)
    # https://stackoverflow.com/questions/74541109/

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


def _shuffle_2D(x):
    return _shuffled(_shuffled(x.swapaxes(0, 1)).swapaxes(0, 1))


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
