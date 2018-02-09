"""
The Delboeuf illusion.
"""

import numpy as np
import pandas as pd
import neuropsydia as n




def delboeuf_compute(distance=5, distance_auto = True, inner_size_smaller=3, outer_size_smaller=0, location_smaller="left", real_difference_ratio=0, illusion_strength=0):
    """
    """

    inner_size_larger = inner_size_smaller*(real_difference_ratio+1)
    outer_size_smaller = (inner_size_smaller + (inner_size_larger/10))*(outer_size_smaller+1)
    outer_size_larger = inner_size_larger + (inner_size_larger/10)

    if illusion_strength < 0:
        illusion_type = "Incongruent"
        outer_size_larger = outer_size_larger + (outer_size_larger * abs(illusion_strength))
    else:
        illusion_type = "Congruent"
        outer_size_smaller = outer_size_smaller + (outer_size_smaller * abs(illusion_strength))



    if distance_auto is False:
        distance_centers = distance
        position_left = 0 - distance_centers/2
        position_right = 0 + distance_centers/2
        distance_edges_inner = distance_centers - (inner_size_smaller/2 + inner_size_larger/2)
        distance_edges_outer = distance_centers - (outer_size_smaller/2 + outer_size_larger/2)
    else:
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (outer_size_smaller/2 + outer_size_larger/2)
        distance_edges_inner = distance_centers - (inner_size_smaller/2 + inner_size_larger/2)
        position_left = 0-distance_centers/2
        position_right = 0+distance_centers/2



    if location_smaller == "left":
        inner_left_size = inner_size_smaller
        inner_right_size = inner_size_larger
        outer_left_size = outer_size_smaller
        outer_right_size = outer_size_larger
    else:
        inner_left_size = inner_size_larger
        inner_right_size = inner_size_smaller
        outer_left_size = outer_size_larger
        outer_right_size = outer_size_smaller



    parameters = {"Distance_Centers": distance_centers,
                  "Distance_Edges_Inner": distance_edges_inner,
                  "Auto_Distance": distance_auto,
                  "Position_Left": position_left,
                  "Position_Right": position_right,

                  "Size_Inner_Smaller": inner_size_smaller,
                  "Size_Inner_Larger": inner_size_larger,
                  "Size_Outer_Smaller": outer_size_smaller,
                  "Size_Outer_Larger": outer_size_larger,
                  "Size_Inner_Left": inner_left_size,
                  "Size_Inner_Right": inner_right_size,
                  "Size_Outer_Left": outer_left_size,
                  "Size_Outer_Right": outer_right_size,

                  "Real_Difference_Inner_Ratio": inner_size_larger/inner_size_smaller-1,
                  "Real_Difference_Inner_Difference": inner_size_larger-inner_size_smaller,
                  "Real_Difference_Outer_Ratio": inner_size_larger/outer_size_smaller-1,
                  "Real_Difference_Outer_Difference": inner_size_larger-outer_size_smaller,

                  "Real_Location_Smaller": location_smaller,
                  "Illusion_Strength_Absolute": abs(illusion_strength),
                  "Illusion_Strength": illusion_strength,
                  "Illusion_Type": illusion_type
                  }

    return(parameters)




def delboeuf_display(parameters=None):
    """
    """
    n.circle(x=parameters["Position_Left"], size=parameters["Size_Outer_Left"], fill_color="white", line_color="black", thickness=0.05)
    n.circle(x=parameters["Position_Left"], size=parameters["Size_Inner_Left"], fill_color="red", line_color="white")
    n.circle(x=parameters["Position_Right"], size=parameters["Size_Outer_Right"], fill_color="white", line_color="black", thickness=0.05)
    n.circle(x=parameters["Position_Right"], size=parameters["Size_Inner_Right"], fill_color="red", line_color="white")






