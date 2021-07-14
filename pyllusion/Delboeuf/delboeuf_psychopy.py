import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..image import image_circle
from ..psychopy.psychopy_circle import psychopy_circle
from .delboeuf_parameters import _delboeuf_parameters


def _delboeuf_psychopy(window, parameters=None, **kwargs):
    """Create a PsychoPy stimulus of the Delboeuf illusion.


    The Delboeuf illusion is an optical illusion of relative size perception,
    where circles of identical size appear as different because of their surrounding context.

    Parameters
    ----------
    window : object
        The window object in which the stimulus will be rendered.
    parameters : dict
        Parameters of the Delbeouf illusion generated by `delboeuf_parameters()`.
    **kwargs
        Additional arguments passed into `delboeuf_parameters()`.

    Returns
    -------
    In-place modification of the PsychoPy window (No explicit return).

    Examples
    ---------
    >>> import pyllusion
    >>> from psychopy import visual, event

    >>> # Create parameters
    >>> parameters = pyllusion.delboeuf_parameters(illusion_strength=1, difference=2)

    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], winType='pygame', color='white')

    >>> # Display illusion
    >>> pyllusion.delboeuf_psychopy(window=window, parameters=parameters)

    >>> # Refresh and close window
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()
    """

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _delboeuf_parameters(**kwargs)

    # Loop circles
    for side in ["Left", "Right"]:
        # Draw outer circle
        size_outer = parameters["Size_Outer_" + side]
        psychopy_circle(
            window,
            x=parameters["Position_" + side],
            y=0,
            size=size_outer,
            color="white",
            outline_color="black",
            outline=3,
        )

        # Draw inner circle
        size_inner = parameters["Size_Inner_" + side]
        psychopy_circle(
            window,
            x=parameters["Position_" + side],
            y=0,
            size=size_inner,
            color="red",
            outline_color="red",
            outline=0.5,
        )