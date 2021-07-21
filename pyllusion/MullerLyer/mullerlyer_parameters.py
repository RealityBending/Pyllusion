import numpy as np

from ..image.utilities import _coord_line
from ..Ponzo.ponzo_parameters import _ponzo_parameters_topbottom


def _mullerlyer_parameters(illusion_strength=0, difference=0, size_min=0.5, distance=1):

    parameters = _ponzo_parameters_topbottom(difference=difference, size_min=size_min, distance=distance)

    length = size_min/2

    if difference >= 0:
        angle = {"Top": illusion_strength, "Bottom": -illusion_strength}
    else:
        angle = {"Top": -illusion_strength, "Bottom": illusion_strength}

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
                       "Illusion_Strength": illusion_strength,
                       "Illusion_Type": "Incongruent" if illusion_strength > 0 else "Congruent",
                       "Distractor_Length": length})

    return parameters
  