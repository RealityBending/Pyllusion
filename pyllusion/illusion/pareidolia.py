import numpy as np
import PIL.Image

from ..image import rescale
from ..image.image_blobs import _image_blob


def pareidolia(n_layers=3, sd=[8, 16, 32], width=500, height=500):
    """
    Create pure-noise images using bivariate Gaussian blobs with different standard deviations (SD).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> ill.pareidolia(n_layers=2, sd=[8, 16])  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>

    """
    array = np.zeros((height, width))
    for layer in range(n_layers):
        array_layer = np.zeros((height, width))
        sd_layer = sd[layer]
        n = int((width / (sd_layer**2 * .15))**2)  # square sd to decrease n
        weight = 5**layer
        for _ in range(n):
            x = np.random.randint(width)
            y = np.random.randint(height)
            blob = _image_blob(x=x, y=y, width=width, height=height, sd=sd_layer)
            array_layer += blob
        array += weight * array_layer

    array = rescale(array, to=[0, 255])
    image = PIL.Image.fromarray(array.astype(np.uint8))
    return image
