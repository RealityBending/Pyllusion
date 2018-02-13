"""
The Zollner illusion.
"""
from . import pyllusion_path

import numpy as np
import pandas as pd
import neuropsydia as n



def zollner_compute(difficulty=0, illusion=0):
    """
    Zollner Illusion

    Parameters
    ----------
    difficulty : float
        Top line angle (clockwise).
    illusion : float
        Top distractor lines angle (clockwise).
    """

    if difficulty > 0:
        slope = illusion
    else:
        slope = -1*illusion


    if illusion > 0:
        illusion_type = "Incongruent"
    else:
        illusion_type = "Congruent"




    slope = np.tan(np.radians(slope+90))
    x = 1/slope

    x1 = -x*1.5
    y1 = -1*1.5
    x2 = x*1.5
    y2 = 1*1.5


    parameters = {"Distractor_Left_x": x1,
                  "Distractor_Left_y": y1,
                  "Distractor_Right_x": x2,
                  "Distractor_Right_y": y2,
                  "Distractor_Slope": slope,
                  "Distractor_Thickness": 25,
                  "Top_Line_Angle": difficulty,
                  "Bottom_Line_Angle": -difficulty,
                  "Top_Line_x": -0.25,
                  "Bottom_Line_x": 0.25,
                  "Top_Line_y": 2.5,
                  "Bottom_Line_y": -2.5,
                  "Top_Line_size": 30,
                  "Bottom_Line_size": 30,
                  "Difficulty": difficulty,
                  "Difficulty_Absolute": abs(difficulty),
                  "Illusion": illusion,
                  "Illusion_Absolute": abs(illusion),
                  "Illusion_Type": illusion_type}

    return(parameters)



def zollner_display(parameters):
    """
    """
    n.image(pyllusion_path + "line_red.png", x=parameters["Top_Line_x"], y=parameters["Top_Line_y"], size=parameters["Top_Line_size"], rotate=-parameters["Top_Line_Angle"], scale_by="width")
    n.image(pyllusion_path + "line_red.png", x=parameters["Bottom_Line_x"], y=parameters["Bottom_Line_y"], size=parameters["Bottom_Line_size"], rotate=-parameters["Bottom_Line_Angle"], scale_by="width")


    for i in range (15):
        n.line(left_x=-7.25+i+parameters["Distractor_Left_x"], left_y=2.5+parameters["Distractor_Left_y"], right_x=-7.25+i+parameters["Distractor_Right_x"], right_y=2.5+parameters["Distractor_Right_y"], line_color="black", thickness=parameters["Distractor_Thickness"])
    for i in range (15):
        n.line(left_x=-6.75+i-parameters["Distractor_Left_x"], left_y=-2.5+parameters["Distractor_Left_y"], right_x=-6.75+i-parameters["Distractor_Right_x"], right_y=-2.5+parameters["Distractor_Right_y"], line_color="black", thickness=parameters["Distractor_Thickness"])



