# -*- coding: utf-8 -*-
from ..image.utilities import _coord_line


def psychopy_line(window, x=0, y=0, x1=None, y1=None, x2=None, y2=None, length=1,
                  rotate=0, size=1, color="black", blur=0,
                  adjust_width=False, adjust_height=False):
    """
    Examples
    --------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event
    
    >>> # Initiate window
    >>> window = visual.Window(size=[800, 600], fullscr=False,
                               screen=0, winType='pygame', monitor='testMonitor',
                               allowGUI=False, allowStencil=False, 
                               color="white", colorSpace='rgb',
                               blendMode='avg', useFBO=True, units='norm')

    >>> # Draw line
    >>> ill.psychopy_line(window, x=0, y=0, length=1)
    
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
    coord, leng, angle = _coord_line(image=None, x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2,
                                     length=length, angle=rotate,
                                     adjust_width=adjust_width, adjust_height=adjust_height)

    # Line parameters
    line = visual.Line(win=window, units='norm', lineColor=color, lineWidth=size)
    line.start = [coord[0], coord[1]]
    line.end = [coord[2], coord[3]]
    
    # blur
    if blur > 0:
        line.opacity = blur
    
    # Display
    line.draw()
