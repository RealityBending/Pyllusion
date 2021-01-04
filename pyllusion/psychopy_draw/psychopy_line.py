# -*- coding: utf-8 -*-
from ..image.utilities import _coord_line
from psychopy import visual, event, core


def psychopy_line(width=800, height=600, x=0, y=0, x1=None, y1=None, x2=None, y2=None, length=1,
                  rotate=0, size=1, color="black", background="white", window=None,
                  blur=0, full_screen=False, adjust_width=False, adjust_height=False):
    """
    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> window = ill.psychopy_line(x=0, y=0, length=1)
    """

    # Draw window
    win = visual.Window(size=[width, height], fullscr=full_screen,
                        screen=0, winType='pyglet', allowGUI=False,
                        allowStencil=False,
                        monitor='testMonitor', color=background, colorSpace='rgb',
                        blendMode='avg', useFBO=True, units='norm')

    # Get coordinates
    coord, leng, angle = _coord_line(image=window, x=x, y=y, x1=x1, y1=y1, x2=x2, y2=y2,
                                     length=length, angle=rotate,
                                     adjust_width=adjust_width, adjust_height=adjust_height)

    # Line parameters
    line = visual.Line(win=win, units='norm', lineColor=color, lineWidth=size)
    line.start = [coord[0], coord[1]]
    line.end = [coord[2], coord[3]]
    
    # blur
    if blur > 0:
        line.opacity = blur
    
    # Display
    while True:
        line.draw()
        win.flip()
    
        if 'escape' in event.getKeys():
            win.close()
            core.quit()
    