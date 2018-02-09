"""
The Ponzo illusion.
"""
from . import pyllusion_path

import numpy as np
import pandas as pd
import neuropsydia as n



def zollner_compute(illusion_strength=0, real_angle=0):
    """
    """
    parameters = {"Illusion_Strength": illusion_strength,
                  "Difficulty": abs(real_angle),
                  "Real_Angle": real_angle,
                  "Real_Angle_Absolute": abs(real_angle)}

    return(parameters)



def zollner_display(parameters):
    """
    """
#    n.line(left_x=-5, left_y=2, right_x=5, right_y=2, line_color="black", thickness=3)
#    n.line(left_x=-5, left_y=-2, right_x=5, right_y=-2, line_color="black", thickness=3)

    n.image(pyllusion_path + "line.png", x=0, y=2, size=18.2, rotate=parameters["Real_Angle"]/2, scale_by="width")
    n.image(pyllusion_path + "line.png", x=0, y=-2, size=18.2, rotate=-parameters["Real_Angle"]/2, scale_by="width")



    for i in range (11):
        n.line(left_x=-6+i+parameters["Illusion_Strength"], left_y=3, right_x=-4+i-parameters["Illusion_Strength"], right_y=1, line_color="black", thickness=6)
#        n.image("rod.png", x=-5+i, y=-2, size=1)
    for i in range (11):
        n.line(left_x=-6+i+parameters["Illusion_Strength"], left_y=-3, right_x=-4+i-parameters["Illusion_Strength"], right_y=-1, line_color="black", thickness=6)






