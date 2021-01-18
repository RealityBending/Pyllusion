# -*- coding: utf-8 -*-
from psychopy import core, event, visual

from ..image.utilities import _coord_text


def psychopy_text(window, text="Hello", width=500, height=500,
                  x=0, y=0, size=10, color="black", background="white",
                  font="arial.ttf", alpha=0, rotate=0, bold=False, italic=False):
    """
    Examples
    --------
    >>> import pyllusion as ill
    >>>
    >>> window = ill.psychopy_text(text="Hello", size=40)  #doctest: +SKIP
    >>> window = ill.psychopy_text(size=30, y=0.5, text="I'm Red", color="red")  #doctest: +SKIP
    >>> window = ill.psychopy_text(size=20, x=0.5, bold=True, text="Bold and blurred", font="arialbd.ttf", alpha=0.5)  #doctest: +SKIP

    """
    pass


    # # Try loading mne
    # try:
    #     import psychopy
    # except ImportError:
    #     raise ImportError(
    #         "The 'psychopy' module is required for this function to run. ",
    #         "Please install it first (`pip install PsychoPy`).",
    #     )

    # # Draw window
    # win = visual.Window(size=[width, height], fullscr=full_screen,
    #                 screen=0, winType='pyglet', allowGUI=False,
    #                 allowStencil=False,
    #                 monitor='testMonitor', color=background, colorSpace='rgb',
    #                 blendMode='avg', units='pix')

    # # Get coordinates
    # message = visual.TextStim(win=win, text=text, font=font, bold=bold, italic=italic,
    #                           color=color, units='pix', height=size)
    # _, _, x, y = _coord_text(win, text=text, size=size, x=x, y=y, font=font, method="psychopy")
    # message.pos = [x-width/2, y-height/2]

    # # Alpha
    # if alpha > 0:
    #     message.opacity = alpha

    # # Orientation
    # if rotate != 0:
    #     message.ori = rotate

    # # Display
    # while True:
    #     message.draw()
    #     win.flip()

    #     if 'escape' in event.getKeys():
    #         win.close()
    #         core.quit()
