import numpy as np

from ..psychopy.psychopy_rectangle import psychopy_rectangle
from .white_parameters import _white_parameters


def _white_psychopy(window, parameters=None, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _white_parameters(**kwargs)

    # Target 1
    for y in parameters["Target1_y"]:
        psychopy_rectangle(window, x=-0.5, y=y, size_height=parameters["Target_Height"],
                           size_width=0.5, color=parameters["Target1_RGB"],
                           fillColorSpace='rgb255')

    # Background 2 and Target 2
    for y in parameters["Target2_y"]:    
        psychopy_rectangle(window, x=0, y=y, size_height=parameters["Target_Height"],
                           size_width=2, color=parameters["Background2_RGB"],
                           fillColorSpace='rgb255', )

        psychopy_rectangle(window, x=0.5, y=y, size_height=parameters["Target_Height"],
                           size_width=0.5, color=parameters["Target2_RGB"],
                           fillColorSpace='rgb255')
