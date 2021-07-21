import numpy as np

from ..psychopy.psychopy_circle import psychopy_circle
from .ebbinghaus_parameters import _ebbinghaus_parameters


def _ebbinghaus_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _ebbinghaus_parameters(**kwargs)

    # Loop circles
    for side in ["Left", "Right"]:
        _ebbinghaus_psychopy_draw(window,
                                  parameters,
                                  side=side,
                                  color_inner="red",
                                  color_outer="black")


def _ebbinghaus_psychopy_draw(window, p, side="Left", color_inner="red", color_outer="black"):

    # Draw inner circle
    psychopy_circle(window, size=p["Size_Inner_" + side], x=p["Position_" + side], y=0,
                    color=color_inner, outline_color=color_inner, outline=0.5)

    # Get width/height ratio to have equidistant circles
    ratio = window.size[0] / window.size[1]

    # Adjust for non-squared screen
    x = p["Position_Outer_x_" + side] / ratio
    x = x + (p["Position_" + side] - np.mean(x))

    # Plot each outer circles
    for i in range(len(p["Position_Outer_x_" + side])):
        psychopy_circle(window, size=p["Size_Outer_" + side],
                        x=x[i], y=p["Position_Outer_y_" + side][i],
                        color=color_outer, outline_color=color_outer, outline=0.5)
