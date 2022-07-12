import numpy as np

from ..image.utilities import _coord_line


def _poggendorff_parameters(illusion_strength=0, difference=0):

    y_offset = difference

    if difference < 0:
        angle = 90 + illusion_strength
    else:
        angle = 90 - illusion_strength
    # Coordinates of left line
    coord, _, _ = _coord_line(x1=0, y1=0, angle=-angle, length=0.75)
    left_x1, left_y1, left_x2, left_y2 = coord

    # Right line
    coord, _, _ = _coord_line(x1=0, y1=y_offset, angle=180 - angle, length=0.75)
    right_x1, right_y1, right_x2, right_y2 = coord

    # Congruency
    if np.sign(difference) != np.sign(illusion_strength):
        congruency = "Congruent"
    else:
        congruency = "Incongruent"

    parameters = {
        "Illusion": "Poggendorff",
        "Illusion_Strength": illusion_strength,
        "Difference": difference,
        "Illusion_Type": congruency,
        "Left_x1": left_x1,
        "Left_y1": left_y1,
        "Left_x2": left_x2,
        "Left_y2": left_y2,
        "Right_x1": right_x1,
        "Right_y1": right_y1,
        "Right_x2": right_x2,
        "Right_y2": right_y2,
        "Angle": angle,
        "Rectangle_Height": 1.75,
        "Rectangle_Width": 0.5,
    }

    return parameters
