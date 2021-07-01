from ..image.utilities import _coord_line


def psychopy_line(window, x=0, y=0, x1=None, y1=None, x2=None, y2=None, length=1,
                  size=1, rotate=0, color="black", alpha=0,
                  adjust_width=False, adjust_height=False, **kwargs):
    """
    Creates a PsychoPy stimulus of a line.


    The `*_line` functions are meant to facilitate the creation of primitive shapes,
    in this case, line(s), that can be assembled into illusory stimuli.

    This function is intended to create lines similar to `image_line()` within PsychoPy.
    It is essentially a wrapper around PsychoPy `psychopy.visual.Line()`. The difference lies
    within the names of the arguments and the values that they take (e.g., we use a consistent
    x-y plane [-1, 1; -1, 1] for the screen "space" with 0 as the center, instead of pixels starting
    from the corner). The purpose of this wrapper is to have consistent behaviour for functions that
    are based on the different backends (e.g., PIL, PsychoPy). See the PsychoPy documentation
    for more information (https://www.psychopy.org/api/visual/line.html).

    Parameters
    ----------
    window: object
        A PsychoPy window for displaying one or more stimuli.
    x : int
        x-coordinates of the center of the line, from -1 to 1.
    y : int
        y-coordinates of the center of the line, from -1 to 1.
    x1, x2 : int
        x-coordinates of the ends of the line, from -1 to 1. If not None, x is set to None.
    y1, y2 : int
        y-coordinates of the ends of the line, from -1 to 1. If not None, y is set to None.
    length : int
        Length of the line returned.
    size : int
        Width of the line returned.
    rotate : float
        The orientation of the line in degrees, 0 being vertical and
        positive values rotating clockwise.
    color : Union[list, str]
        The color of the line as single string value or [r, g, b] list, in which
        colorSpace='rgb255' argument has to be added.
    alpha : float
        The opacity of the line relative to the background, from 1.0 (opaque) to
        0.0 (transparent).
    adjust_width : bool
        If set to True, the x-coordinates of the line can be adjusted
        to the height and width of the window. Defaults to False.
    adjust_height : bool
        If set to True, the y-coordinates of the line can be adjusted
        to the height and width of the window. Defaults to False.
    **kwargs
        Additional arguments passed into `psychopy.visual.Line()`

    Returns
    -------
    In-place modification of the PsychoPy window (No explicit return).

    See Also
    --------
    image_line

    Examples
    --------
    >>> import pyllusion
    >>> from psychopy import visual, event

    >>> # Initiate window
    >>> window = visual.Window(size=[800, 600], winType='pygame', color="white")

    >>> # Draw line
    >>> pyllusion.psychopy_line(window, x=0, y=0, length=1)

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
    coord, leng, angle = _coord_line(image=window, x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2,
                                     length=length, angle=rotate,
                                     adjust_width=adjust_width, adjust_height=adjust_height,
                                     method="psychopy")

    # Line parameters
    line = visual.Line(win=window, units='pix', lineColor=color, lineWidth=size, **kwargs)
    line.start = [coord[0]-window.size[0]/2, coord[1]-window.size[1]/2]
    line.end = [coord[2]-window.size[0]/2, coord[3]-window.size[1]/2]

    # blur
    if alpha > 0:
        line.opacity = alpha

    # Display
    line.draw()
