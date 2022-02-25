import numpy as np


def analyze_color(image, average=True):
    """Amount of Color in an image

    Compute the amount of color in an image (redness, greenness, blueness).

    Parameters
    ----------
    image : ndarray
        Array for R, G and B channels.
    average : bool
        If True, will average the color values of each pixel.

    Returns
    ----------
    dict
        Contains "Redness", "Greenness" and "Blueness" and more (TODO: document this list).

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
    >>> out = pyllusion.analyze_color(image, average=True)
    >>> out["Redness"]
    >>>
    >>> # Get luminance per pixel
    >>> out = pyllusion.analyze_color(image, average=False)
    >>> # Visualize: plt.imshow(out["Redness"], cmap="Reds")

    """
    try:
        import skimage.color
    except ImportError:
        raise ImportError(
            "Pyllusion error: analyze_color(): the 'scikit-image' module is required for this function to run. ",
            "Please install it first (`pip install scikit-image`).",
        )

    out = {}

    # Convert to color space HSL (Hue, saturation, luminance)
    hsv = skimage.color.rgb2hsv(image)

    # Saturation and Luminance
    out["Saturation"] = hsv[:, :, 1]
    out["Brightness"] = hsv[:, :, 2]

    # Get HUE
    hue = np.radians(hsv[:, :, 0] * 360)

    # Redness (peaks at 0°)
    redness = np.rad2deg(_difference_between_angle(hue, np.radians(0)))
    out["Redness"] = 1 - np.abs(redness / 180)

    # Yellowness (peaks at 60)
    yellowness = np.rad2deg(_difference_between_angle(hue, np.radians(60)))
    out["Yellowness"] = 1 - np.abs(yellowness / 180)

    # Blueness (peaks at 240)
    blueness = np.rad2deg(_difference_between_angle(hue, np.radians(240)))
    out["Blueness"] = 1 - np.abs(blueness / 180)

    # Greenness (peaks at 120)
    greenness = np.rad2deg(_difference_between_angle(hue, np.radians(120)))
    out["Greenness"] = 1 - np.abs(greenness / 180)

    lab = skimage.color.rgb2lab(image)
    out["RedGreen"] = lab[:, :, 1]
    out["BlueYellow"] = lab[:, :, 2]

    # Average all elements
    if average is True:
        out = {key: np.mean(value) for (key, value) in out.items()}

    return out


def _difference_between_angle(x, y):
    """Compute the angular difference between two angles (in radians)"""
    vals = np.array([y - x, y - x + 2 * np.pi, y - x - 2 * np.pi])
    idx = np.argmin(np.abs(vals), axis=0)
    return np.take_along_axis(vals, np.array([idx]), axis=0)[0]
