import numpy as np
import PIL.Image

from ..image.image_blobs import image_blobs


def pareidolia(pattern=None, n=[10, 1000], sd=[20, 2], weight=[2, 1], alpha=80, blur=30, negative=False):
    """Create (pseudo)noise images.

    Pareidolia is the tendency to incorrectly perceive of a stimulus as an object
    pattern or meaning known to the observer. To create stimuli for the observation
    of such phenomenon, this function creates pure-noise images using bivariate
    Gaussian blobs with different standard deviations (SD).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> ill.pareidolia((480, 480), n=[20, 300, 4000], sd=[4, 2, 1], weight=[3, 2, 1])  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>

    """
    # Load pattern
    if pattern is None:
        pattern = PIL.Image.new("RGBA", (500, 500), "WHITE")
    elif isinstance(pattern, tuple):
        pattern = PIL.Image.new("RGBA", pattern, "WHITE")
    elif isinstance(pattern, PIL.Image.Image) is False:
        pattern = PIL.Image.open(pattern)
    width, height = pattern.size

    # Convert to black and white RGB (with white background)
    img = PIL.Image.new("RGBA", pattern.size, "WHITE")
    img.paste(pattern, (0, 0), pattern)
    img = img.convert('RGB')

    # Make it negative if need be
    if negative is True:
        img = PIL.ImageOps.invert(img)

    # Blur the image
    img = img.filter(PIL.ImageFilter.GaussianBlur(blur / 100 * width))

    # Generate noise
    sd = np.array(sd) / 100 * width
    noise = image_blobs(img.size, n=n, sd=sd, weight=weight).convert("RGB")

    # Blend with noise
    stim = PIL.Image.blend(img, noise, alpha=alpha / 100)

    # Normalize
    stim = PIL.ImageOps.autocontrast(stim)

    return stim



# def pareidolia(n_layers=3, sd=[8, 16, 32], width=500, height=500):
#     """Create pure-noise images.

#     Pareidolia is the tendency to incorrectly perceive of a stimulus as an object
#     pattern or meaning known to the observer. To create stimuli for the observation
#     of such phenomenon, this function creates pure-noise images using bivariate
#     Gaussian blobs with different standard deviations (SD).

#     Examples
#     ---------
#     >>> import pyllusion as ill
#     >>>
#     >>> ill.pareidolia(n_layers=2, sd=[8, 16])  #doctest: +ELLIPSIS
#     <PIL.Image.Image ...>

#     """
#     array = np.zeros((height, width))
#     for layer in range(n_layers):
#         array_layer = np.zeros((height, width))
#         sd_layer = sd[layer]
#         n = int((width / (sd_layer ** 2 * 0.15)) ** 2)  # square sd to decrease n
#         weight = 5 ** layer
#         for _ in range(n):
#             x = np.random.randint(width)
#             y = np.random.randint(height)
#             blob = _image_blob(x=x, y=y, width=width, height=height, sd=sd_layer)
#             array_layer += blob
#         array += weight * array_layer

#     array = rescale(array, to=[0, 255])
#     image = PIL.Image.fromarray(array.astype(np.uint8))
#     return image
