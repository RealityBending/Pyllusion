from ..image.utilities import _coord_circle
from psychopy import visual, event, core
import numpy as np


def psychopy_circle(
    width=800,
    height=600,
    x=0,
    y=0,
    size=1,
    color="black",
    outline=1,
    color_outline="copy",
    alpha=0,
    blur=0,
    antialias=True,
    window=None,
    background="white",
    full_screen=False
):
    """
    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> window = ill.psychopy_circle()
    >>> window = ill.psychopy_circle(color="red", outline=2, color_outline='black', x=0.5, size=0.5)
    >>> window = ill.psychopy_circle(color="blue", x=-0.3, size=0.5, blur=0.2, alpha=0.5)
    >>> window = ill.psychopy_circle(color="yellow", y=0.5)

    """

    # Draw window
    win = visual.Window(size=[width, height], fullscr=full_screen,
                        screen=0, winType='pyglet', allowGUI=False,
                        allowStencil=False,
                        monitor='testMonitor', color=background, colorSpace='rgb',
                        blendMode='avg', units='pix')
    
    # Get coordinates
    radius, x, y = _coord_circle(image=win, diameter=size, x=x, y=y, method="psychopy")
    
    
    # Circle parameters
    ## Draw circle if blur = 0
    if blur == 0:
        circle = visual.Circle(win=win, radius=radius,
                               units="pix", fillColor=color, lineWidth=outline,
                               edges=radius*2, interpolate=antialias)
        circle.pos = [x-width/2, y-height/2]

        if alpha > 0:
            circle.opacity = alpha
        if outline != 0:
            if color_outline == "copy":
                circle.lineColor = color # border outline to be same as fill color
            else:
                circle.lineColor = color_outline
    
    ## Draw grating if blur > 0
    elif blur > 0:
        grating = visual.GratingStim(
        tex=np.ones([int(radius*2), int(radius*2)]),
        win=win,
        units="pix",
        size=[radius*2, radius*2],
        mask='raisedCos',
        color=color,
    )
        grating.maskParams = {'fringeWidth': blur}
        grating.pos = [x-width/2, y-height/2]
    
        if alpha > 0:
            grating.opacity = alpha

    # Display
    while True:
        if blur == 0:
            circle.draw()
        elif blur > 0:
            grating.draw()
        win.flip()
    
        if 'escape' in event.getKeys():
            win.close()
            core.quit()
