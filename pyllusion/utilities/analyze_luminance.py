import numpy as np


def analyze_luminance(image, average=True):
    """Image Luminance

    Compute the average luminance of an image.

    - Linear Luminance (L): linear measure of light, spectrally weighted for normal vision but not adjusted for the non-linear perception of lightness.
    - Perceived Luminance (L*): non-linear measure of perceptual lightness that approximates the human vision non-linear response curve.

    Parameters
    ----------
    image : ndarray
        Array for R, G and B channels.
    average : bool
        If True, will average the luminance value of each pixel.

    Returns
    ----------
    dict
        Contains "Luminance" and "Luminance_Perceived".

    See Also
    ----------
    - http://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color

    Example
    ----------
    >>> import pyllusion
    >>>
    >>> # Generate image (random pixels)
    >>> image = np.random.rand(500, 500, 3) * 255
    >>> image = image.astype(int)
    >>> # Visualize: plt.imshow(image, interpolation="nearest")
    >>>
    >>> # Compute luminance
    >>> out = pyllusion.analyze_luminance(image, average=True)
    >>> out["Luminance"]
    >>> out["Luminance_Perceived"]
    >>>
    >>> # Get luminance per pixel
    >>> out = pyllusion.analyze_luminance(image, average=False)
    >>> # Visualize: plt.imshow(-1*out["Luminance"], cmap="Greys")

    """
    out = {}
    # 1. Convert all sRGB integers to decimal 0-1
    image = image / 255.0

    # 2. Linearize: Convert gamma encoded RGB to a linear value. sRGB (computer standard) requires
    # a power curve of approximately V^2.2
    image[image <= 0.04045] = image[image <= 0.04045] / 12.92
    image[image > 0.04045] = np.power((image[image > 0.04045] + 0.055) / 1.055, 2.4)

    # 3. To find Luminance (Y) apply the standard coefficients for sRGB
    L = 0.2126 * image[:, :, 0] + 0.7152 * image[:, :, 1] + 0.0722 * image[:, :, 2]

    # 4. Perceived lightness
    Lstar = (
        0.299 * image[:, :, 0] ** 2.2
        + 0.587 * image[:, :, 1] ** 2.2
        + 0.114 * image[:, :, 2] ** 2.2
    ) ** (1 / 2.2)
    # Lstar = image.copy()
    # Lstar[Lstar <= 216 / 24389] = Lstar[Lstar <= 216 / 24389] * (24389 / 27)
    # Lstar[Lstar > 216 / 24389] = np.power(Lstar[Lstar > 216 / 24389], 1 / 3) * 116 - 16

    if average is True:
        L = np.mean(L)
        Lstar = np.mean(Lstar)

    return {"Luminance": L, "Luminance_Perceived": Lstar}
