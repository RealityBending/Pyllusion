import numpy as np

from ..psychopy.psychopy_line import psychopy_line
from .zollner_parameters import _zollner_parameters


def _zollner_psychopy(window, parameters=None, target_only=False, **kwargs):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _zollner_parameters(**kwargs)

    # Draw distractor lines
    if target_only is False:
        for i in range(parameters["Distractors_n"]):
            for pos in ["_Top_", "_Bottom_"]:
                psychopy_line(
                    window,
                    x1=parameters["Distractors" + pos + "x1"][i],
                    y1=parameters["Distractors" + pos + "y1"][i],
                    x2=parameters["Distractors" + pos + "x2"][i],
                    y2=parameters["Distractors" + pos + "y2"][i],
                    adjust_height=True,
                    color="black",
                    size=5,
                )

    # Draw target lines
    for pos in ["Bottom", "Top"]:
        psychopy_line(
            window,
            x1=parameters[pos + "_x1"],
            y1=parameters[pos + "_y1"],
            x2=parameters[pos + "_x2"],
            y2=parameters[pos + "_y2"],
            adjust_height=True,
            color="red",
            size=5,
        )
