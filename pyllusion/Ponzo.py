"""
The Ponzo illusion.
"""

import numpy as np
import pandas as pd
import neuropsydia as n



def ponzo_compute(illusion_strength=0, real_difference=0, bottom_line_size=6):
    """
    """
    # Vertical
    distance = abs(illusion_strength) + 0.25

    bottom_line_left_x = 0-bottom_line_size/2
    bottom_line_left_y = -5
    bottom_line_right_x = 0+bottom_line_size/2
    bottom_line_right_y = -5

    if illusion_strength < 0:
        top_line_size = bottom_line_size - (real_difference*bottom_line_size)
    else:
        top_line_size = bottom_line_size + (real_difference*bottom_line_size)



    top_line_left_x = 0-top_line_size/2
    top_line_left_y = bottom_line_left_y + distance
    top_line_right_x = 0+top_line_size/2
    top_line_right_y = bottom_line_left_y + distance

    if top_line_size >= bottom_line_size:
        difficulty_ratio = top_line_size / bottom_line_size
        difficulty_diff = top_line_size - bottom_line_size
    else:
        difficulty_ratio = bottom_line_size / top_line_size
        difficulty_diff = bottom_line_size - top_line_size

    parameters = {"Distance": distance,
                  "Bottom_Line_Left_x": bottom_line_left_x,
                  "Bottom_Line_Left_y": bottom_line_left_y,
                  "Bottom_Line_Right_x": bottom_line_right_x,
                  "Bottom_Line_Right_y": bottom_line_right_y,
                  "Bottom_Line_Size": bottom_line_size,
                  "Top_Line_Left_x": top_line_left_x,
                  "Top_Line_Left_y": top_line_left_y,
                  "Top_Line_Right_x": top_line_right_x,
                  "Top_Line_Right_y": top_line_right_y,
                  "Top_Line_Size": top_line_size,
                  "Difficulty": abs(difficulty_ratio),
                  "Difficulty_Absolute": abs(difficulty_diff),
                  "Illusion_Strength": illusion_strength,
                  "Illusion_Strength_Absolute": abs(illusion_strength)}


    return(parameters)



def ponzo_display(parameters):
    """
    """
    n.line(left_x=-5, left_y=-8, right_x=-1, right_y=8, line_color="black", thickness=3)
    n.line(left_x=1, left_y=8, right_x=5, right_y=-8, line_color="black", thickness=3)

    n.line(left_x=parameters["Bottom_Line_Left_x"], left_y=parameters["Bottom_Line_Left_y"], right_x=parameters["Bottom_Line_Right_x"], right_y=parameters["Bottom_Line_Right_y"], line_color="red", thickness=10)
    n.line(left_x=parameters["Top_Line_Left_x"], left_y=parameters["Top_Line_Left_y"], right_x=parameters["Top_Line_Right_x"], right_y=parameters["Top_Line_Right_y"], line_color="red", thickness=10)





