# -*- coding: utf-8 -*-
from ..image.utilities import _coord_rectangle


def psychopy_rectangle(
    window,
    x=0,
    y=0,
    size_width=1,
    size_height=1,
    rotate=0,
    color="black",
    outline=0,
    outline_color="black",
    alpha=1,
    adjust_width=False,
    adjust_height=False,
    **kwargs,
):
    """
    Creates a PsychoPy stimulus of a rectangle.

    The `*_rectangle` functions are meant to facilitate the creation of primitive shapes,
    in this case, rectangle(s), that can be assembled into illusory stimuli.

    This function is intended to create lines similar to `image_rectangle()` within PsychoPy.
    It is essentially a wrapper around PsychoPy `psychopy.visual.Rect()`. The difference lies
    within the names of the arguments and the values that they take (e.g., we use a consistent
    x-y plane [-1, 1; -1, 1] for the screen "space" with 0 as the center, instead of pixels starting
    from the corner). The purpose of this wrapper is to have consistent behaviour for functions that
    are based on the different backends (e.g., PIL, PsychoPy). See the PsychoPy documentation
    for more information (https://www.psychopy.org/api/visual/rect.html).

    Parameters
    ----------
    window: object
        A PsychoPy window for displaying one or more stimuli.
    x : float
        x-coordinates of the center of the rectangle, from -1 to 1.
    y : float
        y-coordinates of the center of the rectangle, from -1 to 1.
    size_width : float
        The width of the rectangle.
    size_height : float
        The height of the rectangle.
    rotate : float
        The orientation of the rectangle in degrees, 0 being vertical and
        positive values rotating clockwise.
    color : Union[list, str]
        The fill color of the rectangle as single string value or [r, g, b] list, in which
        colorSpace='rgb255' argument has to be added.
    outline : float
        The width of the outline of the rectangle.
    outline_color : Union[list, str]
        The outline color of the rectangle as single string value or [r, g, b] list, in which
        colorSpace='rgb255' argument has to be added.
    alpha : float
        The opacity of the rectangle relative to the background, from 1.0 (opaque) to
        0.0 (transparent).
    adjust_width : bool
        If set to True, the width of the rectangle can be adjusted
        to the height and width of the window. Defaults to False.
    adjust_height : bool
        If set to True, the height of the rectangle can be adjusted
        to the height and width of the window. Defaults to False.
    **kwargs
        Additional arguments passed into `psychopy.visual.Rect()`

    Returns
    -------
    In-place modification of the PsychoPy window (No explicit return).

    See Also
    --------
    image_rectangle

    Examples
    --------
    >>> import pyllusion
    >>> from psychopy import visual, event

    >>> # Initiate window
    >>> window = visual.Window(size=[800, 600], winType='pygame', color="white")

    >>> # Draw rectangle
    >>> pyllusion.psychopy_rectangle(window, x=0, y=0,
                               size_width=0.5, size_height=0.5,
                               color='white',
                               outline_color='black', outline=3, rotate=1)

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

    # Adjust size for screen ratio
    if adjust_width is True:
        size_width = size_width * (window.size[1] / window.size[0])
    if adjust_height is True:
        size_height = size_height * (window.size[0] / window.size[1])

    # Get coordinates
    x1, y1, x2, y2 = _coord_rectangle(image=window, x=x, y=y, size_width=size_width,
                                      size_height=size_height, method="psychopy")

    # Rectangle parameters
    rect = visual.Rect(
        win=window,
        units='pix',
        width=x2-x1,
        height=y2-y1,
        fillColor=color,
        lineWidth=outline,
        **kwargs,
    )
    x = (x1 + x2)/2
    y = (y1 + y2)/2
    rect.pos = [x-window.size[0]/2, y-window.size[1]/2]
    rect.lineColor = outline_color

    # Alpha
    if alpha > 0:
        rect.opacity = alpha

    # Orientation
    if rotate != 0:
        rect.ori = rotate

    # Display
    rect.draw()
