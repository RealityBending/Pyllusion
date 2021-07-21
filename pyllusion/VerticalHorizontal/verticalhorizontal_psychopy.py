import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from .verticalhorizontal_parameters import _verticalhorizontal_parameters



def _verticalhorizontal_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _verticalhorizontal_parameters(**kwargs)

    # Loop lines
    for side in ["Left", "Right"]:
        psychopy_line(window,
                      x1=parameters[side + "_x1"],
                      y1=parameters[side + "_y1"],
                      x2=parameters[side + "_x2"],
                      y2=parameters[side + "_y2"],
                      length=None, rotate=None, adjust_width=True,
                      color="red", size=5)
