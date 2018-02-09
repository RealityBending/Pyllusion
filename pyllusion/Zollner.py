"""
The Ponzo illusion.
"""
#from . import pyllusion_path

import numpy as np
import pandas as pd
import neuropsydia as n



def zollner_compute(illusion_strength=0, real_angle=0):
    """
    """
    if illusion_strength > 0:
        if illusion_strength > 0:
            slope = illusion_strength
        else:
            slope = -1*illusion_strength
    else:
        if illusion_strength > 0:
            slope = -1*illusion_strength
        else:
            slope = illusion_strength
        
        
    slope = np.tan(np.radians(slope+90))
    x = 1/slope
    
    x1 = -x
    y1 = -1
    x2 = x
    y2 = 1
    
    
    parameters = {"Illusion_Strength": illusion_strength,
                  "Distractor_Left_x": x1,
                  "Distractor_Left_y": y1,
                  "Distractor_Right_x": x2,
                  "Distractor_Right_y": y2,
                  "Difficulty": abs(real_angle),
                  "Real_Angle": real_angle,
                  "Real_Angle_Absolute": abs(real_angle)}

    return(parameters)



def zollner_display(parameters):
    """
    """
    n.image("stimuli/line.png", x=0, y=2, size=18.2, rotate=parameters["Real_Angle"]/2, scale_by="width")
    n.image("stimuli/line.png", x=0, y=-2, size=18.2, rotate=-parameters["Real_Angle"]/2, scale_by="width")

    
    for i in range (11):
        n.line(left_x=-5+i+parameters["Distractor_Left_x"], left_y=2+parameters["Distractor_Left_y"], right_x=-5+i+parameters["Distractor_Right_x"], right_y=2+parameters["Distractor_Right_y"], line_color="black", thickness=6)
    for i in range (11):
        n.line(left_x=-5+i-parameters["Distractor_Left_x"], left_y=-2+parameters["Distractor_Left_y"], right_x=-5+i-parameters["Distractor_Right_x"], right_y=-2+parameters["Distractor_Right_y"], line_color="black", thickness=6)






