import numpy as np

from ..Contrast.contrast_parameters import _contrast_parameters_internal


def _white_parameters(difference=0, illusion_strength=0, strips_n=9):

    colors, rgb = _contrast_parameters_internal(
        difference=difference, illusion_strength=illusion_strength
    )

    y = np.linspace(-1, 1, endpoint=False, num=strips_n)  # All strips' top y
    strip_height = 2 / (strips_n)  # With of one strip
    target2_y = y[1::2] + (strip_height / 2)
    target1_y = y[0::2] + (strip_height / 2)

    parameters = {
        "Illusion": "White's",
        "Illusion_Strength": illusion_strength,
        "Difference": difference,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Target1": colors[0],
        "Target2": colors[1],
        "Background1": colors[2],
        "Background2": colors[3],
        "Target1_RGB": rgb[0],
        "Target2_RGB": rgb[1],
        "Background1_RGB": rgb[2],
        "Background2_RGB": rgb[3],
        "Target1_y": target1_y,
        "Target2_y": target2_y,
        "Target_Height": strip_height,
        "Target_n": strips_n,
    }

    return parameters
