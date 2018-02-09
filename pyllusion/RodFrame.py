"""
The Ponzo illusion.
"""
from . import pyllusion_path


import numpy as np
import pandas as pd
import neuropsydia as n



def rodframe_compute(illusion_strength=0, frame_size=10, rod_angle=0, rod_size=6):
    """
    """

    frame_angle=-illusion_strength

    parameters = {"Frame_Angle": frame_angle,
                  "Rod_Angle": rod_angle,
                  "Frame_Size": frame_size,
                  "Rod_Size": rod_size,
                  "Difficulty": 1-(abs(rod_angle)/45),
                  "Illusion_Strength": illusion_strength/45}

    return(parameters)



def rodframe_display(parameters):
    """
    """
    n.image(pyllusion_path + "frame.png", rotate=parameters["Frame_Angle"], size=parameters["Frame_Size"])
    n.image(pyllusion_path + "rod.png", rotate=parameters["Rod_Angle"], size=parameters["Rod_Size"])






