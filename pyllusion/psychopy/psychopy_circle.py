from ..image.utilities import _coord_circle
import numpy as np


def psychopy_circle(
    window,
    x=0,
    y=0,
    size=1,
    color="black",
    outline=1,
    outline_color="black",
    alpha=0,
    blur=0,
    **kwargs,
    ):
    """
    Creates a PsychoPy stimulus of a circle.

    The `*_circle` functions are meant to facilitate the creation of primitive shapes,
    in this case, circle(s), that can be assembled into illusory stimuli.

    This function is intended to create circles similar to `image_circle()` within PsychoPy.
    It is essentially a wrapper around PsychoPy `psychopy.visual.Circle()`. The difference lies
    within the names of the arguments and the values that they take (e.g., we use a consistent
    x-y plane [-1, 1; -1, 1] for the screen "space" with 0 as the center, instead of pixels starting
    from the corner). The purpose of this wrapper is to have consistent behaviour for functions that
    are based on the different backends (e.g., PIL, PsychoPy). See the PsychoPy documentation
    for more information (https://www.psychopy.org/api/visual/circle.html).


    Parameters
    ----------
    window: object
        A PsychoPy window for displaying one or more stimuli.
    x : float
        x-coordinates of the center of the circle, from -1 to 1.
    y : float
        y-coordinates of the center of the circle, from -1 to 1.
    color : Union[list, str]
        The fill color of the circle as single string value or [r, g, b] list, in which
        colorSpace='rgb255' argument has to be added.
    outline : float
        The width of the outline of the circle.
    outline_color : Union[list, str]
        The outline color of the circle as single string value or [r, g, b] list, in which
        colorSpace='rgb255' argument has to be added.
    alpha : float
        The opacity of the circle relative to the background, from 1.0 (opaque) to
        0.0 (transparent).
    blur : float
        The transparency mask that determines the proportion of the patch that will be blurred.
    **kwargs
        Additional arguments passed into `psychopy.visual.Circle()` or `psychopy.visual.GratingStim()`.

    Returns
    -------
    In-place modification of the PsychoPy window (No explicit return).

    See Also
    --------
    image_circles

    Examples
    --------
    >>> import pyllusion
    >>> from psychopy import visual, event

    >>> # Initiate window
    >>> window = visual.Window(size=[800, 600], winType='pygame', color="white")

    >>> # Draw circle
    >>> pyllusion.psychopy_circle(window, color="yellow", y=0.5)

    >>> # Refresh and close window
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()

    """
    # Try loading psychopy
    try:
        from psychopy import visual
    except ImportError:
        raise ImportError(
            "The 'psychopy' module is required for this function to run. ",
            "Please install it first (`pip install PsychoPy`).",
        )

    # Get coordinates
    radius, x, y = _coord_circle(image=window, diameter=size, x=x, y=y, method="psychopy")


    # Circle parameters
    ## Draw circle if blur = 0
    if blur == 0:
        circle = visual.Circle(win=window, units="pix", fillColor=color,
                               lineColor=outline_color, edges=128,
                               radius=radius, lineWidth=outline, **kwargs)
        circle.pos = [x-window.size[0]/2, y-window.size[1]/2]

        if alpha > 0:
            circle.opacity = alpha

        # Display circle
        circle.draw()

    ## Draw grating if blur > 0
    elif blur > 0:
        grating = visual.GratingStim(tex=np.ones([int(radius*2), int(radius*2)]),
                                     win=window,
                                     units="pix",
                                     size=[radius*2, radius*2],
                                     mask='raisedCos',
                                     color=color, **kwargs)
        grating.maskParams = {'fringeWidth': blur}
        # grating.pos = [x-width/2, y-height/2]
        grating.pos = [x-window.size[0]/2, y-window.size[1]/2]

        if alpha > 0:
            grating.opacity = alpha

        # Display circle
        grating.draw()
