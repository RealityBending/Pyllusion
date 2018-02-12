"""
The Ponzo illusion.
"""
from . import pyllusion_path

import numpy as np
import pandas as pd
import neuropsydia as n



def ponzo_compute(difficulty=0, illusion=0, distance=10, bottom_line_length=8, bottom_line_thickness=14, vertical_lines_thickness=5):
    """
    Ponzo Illusion

    Parameters
    ----------
    difficulty : float
        Real difference of top line.
    illusion : float
        Distance between lines.
    bottom_line_size : float
        Bottom line size.
    bottom_line_y : float
        Bottom line vertical position.
    bottom_line_thickness : float
        Horizontal lines' thickness.
    """
    top_line_length = bottom_line_length + (difficulty*bottom_line_length)

    bottom_line_left_x = 0-bottom_line_length/2
    bottom_line_right_x = 0+bottom_line_length/2
    bottom_line_left_y = 0-distance/2
    bottom_line_right_y = 0-distance/2

    top_line_left_x = 0-top_line_length/2
    top_line_right_x = 0+top_line_length/2
    top_line_left_y = 0+distance/2
    top_line_right_y = 0+distance/2

    if difficulty > 0:
        vertical_angle = -1*illusion
    else:
        vertical_angle = illusion

    if illusion > 0:
        illusion_type = "Incongruent"
    else:
        illusion_type = "Congruent"

    larger_line = max([top_line_length, bottom_line_length])
    smallest_line = min([top_line_length, bottom_line_length])

    parameters = {"Distance": distance,
                  "Bottom_Line_Left_x": bottom_line_left_x,
                  "Bottom_Line_Left_y": bottom_line_left_y,
                  "Bottom_Line_Right_x": bottom_line_right_x,
                  "Bottom_Line_Right_y": bottom_line_right_y,
                  "Bottom_Line_Length": bottom_line_length,
                  "Bottom_Line_Thickness": bottom_line_thickness,
                  "Top_Line_Left_x": top_line_left_x,
                  "Top_Line_Left_y": top_line_left_y,
                  "Top_Line_Right_x": top_line_right_x,
                  "Top_Line_Right_y": top_line_right_y,
                  "Top_Line_Length": top_line_length,

                  "Larger_Line_Length": larger_line,
                  "Smallest_Line_Length": smallest_line,

                  "Vertical_Line_Angle": vertical_angle,

                  "Difficulty": difficulty,
                  "Difficulty_Absolute": abs(difficulty),

                  "Difficulty_Ratio": larger_line/smallest_line,
                  "Difficulty_Diff": larger_line-smallest_line,

                  "Illusion": illusion,
                  "Illusion_Absolute": abs(illusion),
                  "Illusion_Type": illusion_type}


    return(parameters)



def ponzo_display(parameters):
    """
    """
#    n.line(left_x=-5, left_y=-8, right_x=-1, right_y=8, line_color="black", thickness=parameters["Vertical_Lines_Thickness"])
#    n.line(left_x=1, left_y=8, right_x=5, right_y=-8, line_color="black", thickness=parameters["Vertical_Lines_Thickness"])
    n.image(pyllusion_path + "line.png", x=-3, y=0, size=20, rotate=-90-parameters["Vertical_Line_Angle"], scale_by="width")
    n.image(pyllusion_path + "line.png", x=3, y=0, size=20, rotate=-90+parameters["Vertical_Line_Angle"], scale_by="width")

    n.line(left_x=parameters["Bottom_Line_Left_x"], left_y=parameters["Bottom_Line_Left_y"], right_x=parameters["Bottom_Line_Right_x"], right_y=parameters["Bottom_Line_Right_y"], line_color="red", thickness=parameters["Bottom_Line_Thickness"])
    n.line(left_x=parameters["Top_Line_Left_x"], left_y=parameters["Top_Line_Left_y"], right_x=parameters["Top_Line_Right_x"], right_y=parameters["Top_Line_Right_y"], line_color="red", thickness=parameters["Bottom_Line_Thickness"])





