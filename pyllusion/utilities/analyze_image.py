import numpy as np

from .analyze_color import analyze_color
from .analyze_luminance import analyze_luminance


def analyze_image(image):
    """Compute Objective Characteristics of an Image

    Compute the physical characteristics of an image.

    Parameters
    ----------
    image : ndarray
        Array for R, G and B channels.

    Returns
    ----------
    dict
        Contains elements from `analyze_luminance()`, `analyze_color()` and more (TODO: document this list).


    Example
    ----------
    >>> import pyllusion
    >>>
    >>> # Generate image (random pixels)
    >>> image = np.random.rand(500, 500, 3) * 255
    >>> image = image.astype(int)
    >>> # Visualize: plt.imshow(image)
    >>>
    >>> # Compute color
    >>> out = pyllusion.analyze_image(image)
    >>> out["Entropy"]

    """
    try:
        import skimage.color
        import skimage.feature
        import skimage.filters
        import skimage.measure
    except ImportError:
        raise ImportError(
            "Pyllusion error: analyze_color(): the 'scikit-image' module is required for this function to run. ",
            "Please install it first (`pip install scikit-image`).",
        )

    out = analyze_luminance(image, average=True)
    out.update(analyze_color(image, average=True))
    out["Entropy"] = skimage.measure.shannon_entropy(image, base=2)
    # SD of the HUE axis (the colors)
    out["Colorfulness"] = np.std(skimage.color.rgb2hsv(image)[:, :, 0])
    # SD of the Luminance axis
    out["Contrast"] = np.std(skimage.color.rgb2lab(image)[:, :, 0])

    # Edge detection
    bw = skimage.color.rgb2gray(image)
    edges = skimage.filters.sobel(bw)  # skimage.filters.roberts or skimage.feature.canny
    out["Structure"] = skimage.measure.shannon_entropy(edges, base=2)
    return out
