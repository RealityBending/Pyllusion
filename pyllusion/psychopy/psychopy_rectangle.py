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
    blur=0,
    adjust_width=False,
    adjust_height=False,
):
    """
    Examples
    --------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event
    
    >>> # Initiate window
    >>> window = visual.Window(size=[800, 600], fullscr=False,
                               screen=0, winType='pygame', monitor='testMonitor',
                               allowGUI=False, color="white",
                               blendMode='avg', units='pix')

    >>> # Draw rectangle
    >>> ill.psychopy_rectangle(window, x=0, y=0, color='white',
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
