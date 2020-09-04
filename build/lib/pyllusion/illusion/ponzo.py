import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line
from ..image.utilities import _coord_line

def ponzo_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.ponzo_parameters(difficulty=0, illusion_strength=20)
    >>> ill.ponzo_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = ponzo_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Distractors lines
    for side in ["Left", "Right"]:
        image = image_line(image=image,
                   x1=parameters[side + "_x1"],
                   y1=parameters[side + "_y1"],
                   x2=parameters[side + "_x2"],
                   y2=parameters[side + "_y2"],
                   color="black",
                   size=outline)

    # Target lines (horizontal)
    for position in ["Bottom", "Top"]:
        image = image_line(image=image,
                   x1=parameters[position + "_x1"],
                   y1=parameters[position + "_y1"],
                   x2=parameters[position + "_x2"],
                   y2=parameters[position + "_y2"],
                   color="red",
                   size=outline)

    return image




# ------------------------------------------
# Parameters
# ------------------------------------------



def ponzo_parameters(difficulty=0, size_min=0.5, illusion_strength=0, distance=1):
    """
    Ponzo Illusion

    Parameters
    ----------
    difficulty : float
        Real difference of top line.
    illusion_strength : float
        Distance between lines.
    minimum_length : float
        Minimum line size.
    bottom_line_y : float
        Bottom line vertical position.
    bottom_line_thickness : float
        Horizontal lines' thickness.
    """
    parameters = _ponzo_parameters_topbottom(difficulty=difficulty, size_min=size_min, distance=distance)

    parameters.update(_ponzo_parameters_leftright(difficulty, illusion_strength))

    parameters.update({"Illusion": "Ponzo"})

    return parameters



def _ponzo_parameters_leftright(difficulty, illusion_strength):
    # Angle of lines
    angle = illusion_strength
    angle = -1 * angle if difficulty > 0 else angle

    # Left line
    left_coord, length, _ = _coord_line(x=-0.5, y=0, length=1, angle=angle)
    left_x1, left_y1, left_x2, left_y2, length = _ponzo_parameters_adjust(left_coord, angle, side="Left")

    # Right line
    right_coord, length, _ = _coord_line(x=0.5, y=0, length=1, angle=-angle)
    right_x1, right_y1, right_x2, right_y2, length = _ponzo_parameters_adjust(right_coord, angle, side="Right")

    parameters = {
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Side_Angle": angle,
        "Side_Length": length,
        "Left_x1": left_x1,
        "Left_y1": left_y1,
        "Left_x2": left_x2,
        "Left_y2": left_y2,
        "Right_x1": right_x1,
        "Right_y1": right_y1,
        "Right_x2": right_x2,
        "Right_y2": right_y2
        }
    return parameters


def _ponzo_parameters_adjust(coord, angle, side="Left"):
    # Modify upper and lower points
    if side == "Left":
        x1, y1, x2, y2 = coord

        # Fix upper y to 0.5
        y2 = 1.1
        x2 = ((y2 - y1) * np.tan(np.deg2rad(angle)) + x1)
        length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

        # Fix lower y to -0.5
        y1 = -1.1
        x1 = -1 * ((y2 - y1) * np.tan(np.deg2rad(angle)) - x2)
        length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    else:
        x1, y1, x2, y2 = coord

        # Fix upper y to 0.5
        y2 = 1.1
        x2 = -1 * ((y2 - y1) * np.tan(np.deg2rad(angle)) - x1)
        length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

        # Fix lower y to -0.5
        y1 = -1.1
        x1 = ((y2 - y1) * np.tan(np.deg2rad(angle)) + x2)
        length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    # Prevent clipping
    if side == "Left":
        if x2 > 0:
            x2 = 0
            y2 = ((x2 - x1) * np.tan(np.deg2rad(90-angle)) + y1)
            length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if x1 > 0:
            x1 = 0
            y1 = -1 * ((x2 - x1) * np.tan(np.deg2rad(90-angle)) - y2)
            length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    else:
        if x2 < 0:
            x2 = 0
            y2 = -1 * ((x2 - x1) * np.tan(np.deg2rad(90-angle)) - y1)
            length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if x1 < 0:
            x1 = 0
            y1 = ((x2 - x1) * np.tan(np.deg2rad(90-angle)) + y2)
            length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    return x1, y1, x2, y2, length





def _ponzo_parameters_topbottom(difficulty=0, size_min=0.5, distance=1):

    if difficulty > 0: # if down is smaller
        bottom_length = size_min
        top_length = (1 + np.abs(difficulty)) * size_min
    else:
        top_length = size_min
        bottom_length = (1 + np.abs(difficulty)) * size_min

    bottom_x1 = -(bottom_length / 2)
    bottom_y1 = -(distance / 2)
    bottom_x2 = bottom_length / 2
    bottom_y2 = -(distance / 2)

    top_x1 = -(top_length / 2)
    top_y1 = distance / 2
    top_x2 = top_length / 2
    top_y2 = distance / 2

    parameters = {"Difficulty": difficulty,
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
                  "Size_Smaller": np.min([top_length, bottom_length])
                  }

    return parameters
