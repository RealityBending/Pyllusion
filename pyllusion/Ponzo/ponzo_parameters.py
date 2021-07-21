import numpy as np

from ..image.utilities import _coord_line


def _ponzo_parameters(illusion_strength=0, difference=0, size_min=0.5, distance=1):

    parameters = _ponzo_parameters_topbottom(
        difference=difference, size_min=size_min, distance=distance
    )

    parameters.update(_ponzo_parameters_leftright(difference, illusion_strength))

    parameters.update({"Illusion": "Ponzo"})

    return parameters


def _ponzo_parameters_leftright(difference, illusion_strength):
    # Angle of lines
    angle = illusion_strength
    angle = -1 * angle if difference > 0 else angle

    # Left line
    left_coord, length, _ = _coord_line(x=-0.5, y=0, length=1, angle=angle)
    left_x1, left_y1, left_x2, left_y2, length = _ponzo_parameters_adjust(
        left_coord, angle, side="Left"
    )

    # Right line
    right_coord, length, _ = _coord_line(x=0.5, y=0, length=1, angle=-angle)
    right_x1, right_y1, right_x2, right_y2, length = _ponzo_parameters_adjust(
        right_coord, angle, side="Right"
    )

    parameters = {
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Incongruent" if illusion_strength > 0 else "Congruent",
        "Side_Angle": angle,
        "Side_Length": length,
        "Left_x1": left_x1,
        "Left_y1": left_y1,
        "Left_x2": left_x2,
        "Left_y2": left_y2,
        "Right_x1": right_x1,
        "Right_y1": right_y1,
        "Right_x2": right_x2,
        "Right_y2": right_y2,
    }
    return parameters


def _ponzo_parameters_adjust(coord, angle, side="Left"):
    # Modify upper and lower points
    if side == "Left":
        x1, y1, x2, y2 = coord

        # Fix upper y to 0.5
        y2 = 1.1
        x2 = (y2 - y1) * np.tan(np.deg2rad(angle)) + x1
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Fix lower y to -0.5
        y1 = -1.1
        x1 = -1 * ((y2 - y1) * np.tan(np.deg2rad(angle)) - x2)
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        x1, y1, x2, y2 = coord

        # Fix upper y to 0.5
        y2 = 1.1
        x2 = -1 * ((y2 - y1) * np.tan(np.deg2rad(angle)) - x1)
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Fix lower y to -0.5
        y1 = -1.1
        x1 = (y2 - y1) * np.tan(np.deg2rad(angle)) + x2
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Prevent clipping
    if side == "Left":
        if x2 > 0:
            x2 = 0
            y2 = (x2 - x1) * np.tan(np.deg2rad(90 - angle)) + y1
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if x1 > 0:
            x1 = 0
            y1 = -1 * ((x2 - x1) * np.tan(np.deg2rad(90 - angle)) - y2)
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        if x2 < 0:
            x2 = 0
            y2 = -1 * ((x2 - x1) * np.tan(np.deg2rad(90 - angle)) - y1)
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if x1 < 0:
            x1 = 0
            y1 = (x2 - x1) * np.tan(np.deg2rad(90 - angle)) + y2
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return x1, y1, x2, y2, length


def _ponzo_parameters_topbottom(difference=0, size_min=0.5, distance=1):

    if difference > 0:  # if down is smaller
        bottom_length = size_min
        top_length = (1 + np.abs(difference)) * size_min
    else:
        top_length = size_min
        bottom_length = (1 + np.abs(difference)) * size_min

    bottom_x1 = -(bottom_length / 2)
    bottom_y1 = -(distance / 2)
    bottom_x2 = bottom_length / 2
    bottom_y2 = -(distance / 2)

    top_x1 = -(top_length / 2)
    top_y1 = distance / 2
    top_x2 = top_length / 2
    top_y2 = distance / 2

    parameters = {
        "Difference": difference,
        "Distance": distance,
        "Bottom_x1": bottom_x1,
        "Bottom_y1": bottom_y1,
        "Bottom_x2": bottom_x2,
        "Bottom_y2": bottom_y2,
        "Top_x1": top_x1,
        "Top_y1": top_y1,
        "Top_x2": top_x2,
        "Top_y2": top_y2,
        "Size_Bottom": bottom_length,
        "Size_Top": top_length,
        "Size_Larger": np.max([top_length, bottom_length]),
        "Size_Smaller": np.min([top_length, bottom_length]),
    }

    return parameters
