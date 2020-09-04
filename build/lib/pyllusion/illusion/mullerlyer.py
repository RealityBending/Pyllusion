import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line
from ..image.utilities import _coord_line
from .ponzo import _ponzo_parameters_topbottom


def mullerlyer_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.mullerlyer_parameters(difficulty=0, illusion_strength=3)
    >>> ill.mullerlyer_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    >>> parameters = ill.mullerlyer_parameters(difficulty=0, illusion_strength=30)
    >>> ill.mullerlyer_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = mullerlyer_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Distractors lines
    for which in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:  #
        for side in ["1", "2"]:
            image = image_line(
                image=image,
                x1=parameters["Distractor_" + which + side + "_x1"],
                y1=parameters["Distractor_" + which + side + "_y1"],
                x2=parameters["Distractor_" + which + side + "_x2"],
                y2=parameters["Distractor_" + which + side + "_y2"],
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



def mullerlyer_parameters(difficulty=0, size_min=0.5, illusion_strength=0, distance=1):
    parameters = _ponzo_parameters_topbottom(difficulty=difficulty, size_min=size_min, distance=distance)

    length = size_min/2

    if difficulty >= 0:
        angle = {"Top": -illusion_strength, "Bottom": illusion_strength}
    else:
        angle = {"Top": illusion_strength, "Bottom": -illusion_strength}

    for which in ["Top", "Bottom"]:
        for side in ["Left", "Right"]:
            if side == "Left":
                coord, _, _ = _coord_line(x1=parameters[which + "_x1"], y1=parameters[which + "_y1"], length=length, angle=angle[which])
            else:
                coord, _, _ = _coord_line(x1=parameters[which + "_x2"], y1=parameters[which + "_y2"], length=length, angle=-angle[which])
            x1, y1, x2, y2 = coord

            for c in ["1", "2"]:
                parameters["Distractor_" + which + side + c + "_x1"] = x1
                parameters["Distractor_" + which + side + c + "_y1"] = y1
                parameters["Distractor_" + which + side + c + "_x2"] = x2
                if c == "1":
                    parameters["Distractor_" + which + side + c + "_y2"] = y2
                else:
                    parameters["Distractor_" + which + side + c + "_y2"] = y2 - 2 * (y2 - y1)


    parameters.update({"Illusion": "MullerLyer",
                       "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
                       "Distractor_Length": length})

    return parameters