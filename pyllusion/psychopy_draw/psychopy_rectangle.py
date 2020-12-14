# -*- coding: utf-8 -*-
from ..image.utilities import _coord_rectangle
from psychopy import visual, event, core


def psychopy_rectangle(
    width=800,
    height=600,
    x=0,
    y=0,
    size_width=1,
    size_height=1,
    rotate=0,
    color="black",
    outline=0,
    color_outline="copy",
    alpha=1,
    blur=0,
    antialias=True,
    window=None,
    background="white",
    adjust_width=False,
    adjust_height=False,
    full_screen=False
):
    """
    Parameters
    ----------

    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> window = ill.psychopy_rectangle(x=0, y=0, color='white', color_outline='black', outline=3, rotate=1)
    >>> window = ill.psychopy_rectangle(x=0.5, size_width=0.5, rotate=45, color="red")
    >>> window = ill.psychopy_rectangle(y=0.25, size_height=0.2, color="yellow", alpha=0.5)
    >>> window = ill.psychopy_rectangle(size_width=0.5, size_height=0.5, blur=0.01, color="green", adjust_width=True)
    """
    # Draw window
    win = visual.Window(size=[width, height], fullscr=full_screen,
                    screen=0, winType='pyglet', allowGUI=False,
                    allowStencil=False,
                    monitor='testMonitor', color=background, colorSpace='rgb',
                    blendMode='avg', units='pix')

    # Adjust size for screen ratio
    if adjust_width is True:
        size_width = size_width * (height / width)
    if adjust_height is True:
        size_height = size_height * (width / height)
    
    # Get coordinates
    x1, y1, x2, y2 = _coord_rectangle(image=win, x=x, y=y, size_width=size_width, size_height=size_height)
    
    # Rectangle parameters
    rect = visual.Rect(
        win=win,
        units='pix',
        width=x2-x1,
        height=y2-y1,
        fillColor=color,
        lineWidth=outline,
        interpolate=antialias,
    )
    x = (x1 + x2)/2
    y = (y1 + y2)/2
    rect.pos = [x-width/2, y-height/2]
    
    # Outline
    if outline != 0:
        if color_outline == "copy":
            rect.lineColor = color # border outline to be same as fill color
        else:
            rect.lineColor = color_outline

    # Alpha
    if alpha > 0:
        rect.opacity = alpha
    
    # Orientation
    if rotate > 0:
        rect.ori = rotate
    
    # Display
    while True:
        rect.draw()
        win.flip()
        
        if 'escape' in event.getKeys():
            win.close()
            core.quit()
