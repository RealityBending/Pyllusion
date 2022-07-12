import numpy as np

from ..image import rescale


def _contrast_parameters(illusion_strength=0, difference=0):

    colors, rgb = _contrast_parameters_internal(
        difference=difference, illusion_strength=illusion_strength
    )

    parameters = {
        "Illusion": "Contrast",
        "Illusion_Strength": illusion_strength,
        "Difference": difference,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Rectangle_Top": colors[0],
        "Rectangle_Bottom": colors[1],
        "Background_Top": colors[2],
        "Background_Bottom": colors[3],
        "Rectangle_Top_RGB": rgb[0],
        "Rectangle_Bottom_RGB": rgb[1],
        "Background_Top_RGB": rgb[2],
        "Background_Bottom_RGB": rgb[3],
    }

    return parameters


def _contrast_parameters_internal(difference=0, illusion_strength=0):
    # Targets
    # A difference of 1 means a difference of 1%
    up = 0.5 + difference / 200
    low = 0.5 - difference / 200

    # Backgrounds
    # A illusion_strength of 1 means a difference of 1%
    mod = np.sign(difference) if difference != 0 else 1
    background_up = 0.5 + mod * illusion_strength / 200
    background_low = 0.5 - mod * illusion_strength / 200

    # Adjustments in case of same contrast between rectangle and background
    if background_up == up:
        if background_up > background_low:
            background_up += 0.01
        elif background_up < background_low:
            background_up -= 0.01
        else:
            background_up -= 0.01
            background_low -= 0.01
    if background_low == low:
        if background_low > background_up:
            background_low += 0.01
        elif background_low < background_up:
            background_low -= 0.01
        else:
            background_low -= 0.01
            background_up -= 0.01

    # Transform to RGB tuples
    background_up_rgb = tuple(
        np.rint(rescale([background_up] * 3, scale=[0, 1], to=[0, 255])).astype(int)
    )
    background_low_rgb = tuple(
        np.rint(rescale([background_low] * 3, scale=[0, 1], to=[0, 255])).astype(int)
    )
    up_rgb = tuple(np.rint(rescale([up] * 3, scale=[0, 1], to=[0, 255])).astype(int))
    low_rgb = tuple(np.rint(rescale([low] * 3, scale=[0, 1], to=[0, 255])).astype(int))

    return (
        (up, low, background_up, background_low),
        (up_rgb, low_rgb, background_up_rgb, background_low_rgb),
    )
