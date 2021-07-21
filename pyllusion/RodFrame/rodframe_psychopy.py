import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from ..psychopy.psychopy_rectangle import psychopy_rectangle
from .rodframe_parameters import _rodframe_parameters


def _rodframe_psychopy(window, parameters=None, **kwargs):
    
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _rodframe_parameters(**kwargs)

    # Frame
    psychopy_rectangle(window, x=0, y=0,
                       size_width=1, size_height=1,
                       color="white", outline_color="black", outline=5,
                       rotate=parameters["Frame_Angle"], adjust_width=True)

    # Rod
    psychopy_line(window, x=0, y=0, length=0.8, rotate=parameters["Rod_Angle"],
                  adjust_width=True, color="red", size=5)
