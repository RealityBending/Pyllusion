# -*- coding: utf-8 -*-
from ..image.utilities import _coord_text


def psychopy_text(window, text="Hello",
                  x=0, y=0, size=10, color="black", font="arial", alpha=0, rotate=0,
                  bold=False, italic=False):
    """
    Examples
    --------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event

    >>> # Initiate window
    >>> window = visual.Window(size=[500, 500], fullscr=False,
                               screen=0, winType='pygame', monitor='testMonitor',
                               allowGUI=False, color="white",
                               blendMode='avg', units='pix')

    >>> # Draw text
    >>> ill.psychopy_text(window, size=40, text="Hello", font="arial.ttf")  #doctest: +SKIP

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
    message = visual.TextStim(win=window, text=text, font=font, bold=bold, italic=italic,
                              color=color, units='pix', height=size)
    _, _, x, y = _coord_text(window, text=text, size=size, x=x, y=y, font=font, method="psychopy")
    message.pos = [x-window.size[0]/2, y-window.size[1]/2]

    # Alpha
    if alpha > 0:
        message.opacity = alpha

    # Orientation
    if rotate != 0:
        message.ori = rotate

    # Display message
    message.draw()
