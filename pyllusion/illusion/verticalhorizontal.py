import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line
from ..image.utilities import _coord_line


def verticalhorizontal_image(
    parameters=None, width=800, height=600, background="white", **kwargs
):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.verticalhorizontal_parameters(difficulty=0, illusion_strength=90)
    >>> ill.verticalhorizontal_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = verticalhorizontal_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Lines
    for side in ["Left", "Right"]:
        image = image_line(
            image=image,
            x1=parameters[side + "_x1"],
            y1=parameters[side + "_y1"],
            x2=parameters[side + "_x2"],
            y2=parameters[side + "_y2"],
            length=None,
            rotate=None,
            color="red",
            size=20,
            adjust_width=True,
        )

    return image


def verticalhorizontal_parameters(difficulty=0, illusion_strength=0, size_min=0.5):
    """
    Rod and Frame Illusion

    Parameters
    ----------
    """
    if difficulty >= 0:  # if right is smaller
        right_length = size_min
        left_length = (1 + np.abs(difficulty)) * size_min
        if illusion_strength >= 0:
            left_angle = -90 + illusion_strength
            right_angle = 90
        else:
            left_angle = -90
            right_angle = 90 + illusion_strength
    else:
        left_length = size_min
        right_length = (1 + np.abs(difficulty)) * size_min
        if illusion_strength >= 0:
            left_angle = -90
            right_angle = 90 - illusion_strength
        else:
            left_angle = -90 - illusion_strength
            right_angle = 90

    left_coord, _, _ = _coord_line(x1=-0.25, y1=0, length=left_length, angle=left_angle)
    left_x1, left_y1, left_x2, left_y2 = left_coord
    right_coord, _, _ = _coord_line(
        x1=0.25, y1=0, length=right_length, angle=right_angle
    )
    right_x1, right_y1, right_x2, right_y2 = right_coord

    # Center y
    ys = np.array([left_y1, left_y2, right_y1, right_y2])
    left_y1, left_y2, right_y1, right_y2 = ys - (np.max(ys) / 2)

    # Center x
    xs = np.array([left_x1, left_x2, right_x1, right_x2])
    centre = np.mean([np.max(xs), np.min(xs)])
    left_x1, left_x2, right_x1, right_x2 = xs - centre

    parameters = {
        "Illusion": "VerticalHorizontal",
        "Size_Left": left_length,
        "Size_Right": right_length,
        "Difficulty": difficulty,
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Left_x1": left_x1,
        "Left_y1": left_y1,
        "Left_x2": left_x2,
        "Left_y2": left_y2,
        "Left_Angle": left_angle,
        "Right_x1": right_x1,
        "Right_y1": right_y1,
        "Right_x2": right_x2,
        "Right_y2": right_y2,
        "Right_Angle": right_angle,
    }

    return parameters
