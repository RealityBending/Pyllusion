"""
The Rod and Frame illusion.
"""
from . import pyllusion_path


import numpy as np
import pandas as pd
import neuropsydia as n


def rodframe_compute(difficulty=0, illusion=0, frame_size=10, rod_size=6):
    """
    Rod and Frame Illusion

    Parameters
    ----------
    difficulty : float
        Rod Angle (clockwise).
    illusion : float
        Frame Angle (clockwise).
    rod_size : float
        Rod Size.
    frame_size : float
        Frame Size.
    """
    rod_angle = difficulty

    if difficulty > 0:
        frame_angle = -1*illusion
    else:
        frame_angle = illusion

    if illusion > 0:
        illusion_type = "Incongruent"
    else:
        illusion_type = "Congruent"

    parameters = {"Frame_Angle": frame_angle,
                  "Rod_Angle": rod_angle,
                  "Frame_Size": frame_size,
                  "Rod_Size": rod_size,
                  "Angle_Difference": rod_angle - frame_angle,
                  "Difficulty": rod_angle,
                  "Difficulty_Absolute": abs(rod_angle),
                  "Illusion": illusion,
                  "Illusion_Absolute": abs(illusion),
                  "Illusion_Type": illusion_type}

    return(parameters)



def rodframe_display(parameters):
    """
    """
    n.image(pyllusion_path + "frame.png", rotate=-1*parameters["Frame_Angle"], size=parameters["Frame_Size"])
    n.image(pyllusion_path + "rod_red.png", rotate=-1*parameters["Rod_Angle"], size=parameters["Rod_Size"])

