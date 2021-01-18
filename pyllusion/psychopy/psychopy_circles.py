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
    blur=0,
    alpha=0,
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

    >>> # Draw circle
    >>> ill.psychopy_circle(window, color="yellow", y=0.5)

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
                               radius=radius, lineWidth=outline)
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
                                     color=color)
        grating.maskParams = {'fringeWidth': blur}
        # grating.pos = [x-width/2, y-height/2]
        grating.pos = [x-window.size[0]/2, y-window.size[1]/2]

        if alpha > 0:
            grating.opacity = alpha

        # Display circle
        grating.draw()
