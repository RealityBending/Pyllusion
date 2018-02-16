"""
The Delboeuf illusion.
"""

import numpy as np
import pandas as pd
import neuropsydia as n




def delboeuf_compute(difficulty=0, illusion=0, inner_size_left=3, distance=5, distance_auto=True, background_color="grey"):
    """
    Delboeuf Illusion

    Parameters
    ----------
    difficulty : float
        Size of right inner circle.
    illusion : float
        Size of outer circles.
    inner_size_left : float
        Size of left inner circle.
    distance : float
        distance between circles.
    distance_auto : bool
        If true, distance is between edges (fixed spacing), if false, between centers (fixed location).
    background_color : str
        Background color.
    """

    inner_size_right = inner_size_left +  inner_size_left * difficulty

    outer_size_left = inner_size_left + (inner_size_left/10)
    outer_size_right = inner_size_right + (inner_size_right/10)

    if difficulty > 0: # if right is larger
        if illusion > 0: # if right is supposed to look smaller
            illusion_type = "Incongruent"
            outer_size_right = outer_size_right + outer_size_right * illusion
        else:
            illusion_type = "Congruent"
            outer_size_left = outer_size_left + outer_size_left * abs(illusion)
    else: # if left is larger
        if illusion > 0: # if left is supposed to look smaller
            illusion_type = "Incongruent"
            outer_size_left = outer_size_left + outer_size_left * illusion
        else:
            illusion_type = "Congruent"
            outer_size_right = outer_size_right + outer_size_right * abs(illusion)

    inner_size_smaller = min([inner_size_left, inner_size_right])
    inner_size_larger = max([inner_size_left, inner_size_right])
    outer_size_smaller = min([outer_size_left, outer_size_right])
    outer_size_larger = max([outer_size_left, outer_size_right])




    if distance_auto is False:
        distance_centers = distance
        position_left = 0 - distance_centers/2
        position_right = 0 + distance_centers/2
        distance_edges_inner = distance_centers - (inner_size_left/2 + inner_size_right/2)
        distance_edges_outer = distance_centers - (outer_size_left/2 + outer_size_right/2)
    else:
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (inner_size_left/2 + inner_size_right/2)
        distance_edges_inner = distance_centers - (outer_size_left/2 + outer_size_right/2)
        position_left = 0-distance_centers/2
        position_right = 0+distance_centers/2



    parameters = {"Illusion": illusion,
                  "Illusion_Absolute": abs(illusion),
                  "Illusion_Type": illusion_type,
                  "Difficulty": difficulty,
                  "Difficulty_Absolute": abs(difficulty),

                  "Difficulty_Ratio": inner_size_larger/inner_size_smaller,
                  "Difficulty_Diff": inner_size_larger-inner_size_smaller,

                  "Size_Inner_Left": inner_size_left,
                  "Size_Inner_Right": inner_size_right,
                  "Size_Outer_Left": outer_size_left,
                  "Size_Outer_Right": outer_size_right,

                  "Distance_Centers": distance_centers,
                  "Distance_Edges_Inner": distance_edges_inner,
                  "Distance_Edges_Outer": distance_edges_outer,
                  "Auto_Distance": distance_auto,

                  "Size_Inner_Smaller": inner_size_smaller,
                  "Size_Inner_Larger": inner_size_larger,
                  "Size_Outer_Smaller": outer_size_smaller,
                  "Size_Outer_Larger": outer_size_larger,


                  "Position_Left": position_left,
                  "Position_Right": position_right,

                  "Background_Color": background_color
                  }

    return(parameters)




def delboeuf_display(parameters=None):
    """
    """
    n.circle(x=parameters["Position_Left"], size=parameters["Size_Outer_Left"], fill_color=parameters["Background_Color"], line_color="black", thickness=0.05)
    n.circle(x=parameters["Position_Left"], size=parameters["Size_Inner_Left"], fill_color="red", line_color="white")
    n.circle(x=parameters["Position_Right"], size=parameters["Size_Outer_Right"], fill_color=parameters["Background_Color"], line_color="black", thickness=0.05)
    n.circle(x=parameters["Position_Right"], size=parameters["Size_Inner_Right"], fill_color="red", line_color="white")






