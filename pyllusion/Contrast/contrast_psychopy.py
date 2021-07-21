import numpy as np

from ..psychopy.psychopy_rectangle import psychopy_rectangle
from .contrast_parameters import _contrast_parameters


def _contrast_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _contrast_parameters(**kwargs)

    # Background lower
    psychopy_rectangle(window, x=0, y=-0.5, size_height=1, size_width=2, color=parameters["Background_Bottom_RGB"],
                       outline_color=parameters["Background_Bottom_RGB"],
                       fillColorSpace='rgb255', lineColorSpace='rgb255')

    psychopy_rectangle(window, x=0, y=0.5, size_height=0.5, size_width=1, color=parameters["Rectangle_Top_RGB"],
                       outline_color=parameters["Rectangle_Top_RGB"],
                       fillColorSpace='rgb255', lineColorSpace='rgb255')

    psychopy_rectangle(window, x=0, y=-0.5, size_height=0.5, size_width=1, color=parameters["Rectangle_Bottom_RGB"],
                       outline_color=parameters["Rectangle_Bottom_RGB"],
                       fillColorSpace='rgb255', lineColorSpace='rgb255')
