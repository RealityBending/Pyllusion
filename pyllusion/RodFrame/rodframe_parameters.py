import numpy as np

from ..image.utilities import _coord_line


def _rodframe_parameters(illusion_strength=0, difference=0):

    rod_angle = -difference

    if difference >= 0:
        frame_angle = illusion_strength
    else:
        frame_angle = -1 * illusion_strength

    parameters = {
        "Illusion": "RodFrame",
        "Frame_Angle": frame_angle,
        "Rod_Angle": rod_angle,
        "Angle_Difference": rod_angle - frame_angle,
        "Difference": difference,
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Incongruent" if illusion_strength > 0 else "Congruent",
    }

    return parameters
