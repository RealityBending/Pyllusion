from ..image.utilities import _coord_circle
from psychopy import visual, event, core


def psychopy_circle(
    width=800,
    height=600,
    x=0,
    y=0,
    size=1,
    color="black",
    outline=1,
    color_outline="copy",
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
    >>> window = ill.psychopy_circle(color="red", color_outline="yellow", x=0.5, size=0.5)
    >>> window = ill.psychopy_circle(color="blue", x=-0.3, size=0.5, blur=0.05)
    >>> window = ill.psychopy_circle(color="yellow", y=0.5, blur=0.5)

    """

    # Draw window
    win = visual.Window(size=[width, height], fullscr=full_screen,
                        screen=0, winType='pyglet', allowGUI=False,
                        allowStencil=False,
                        monitor='testMonitor', color=background, colorSpace='rgb',
                        blendMode='avg', units='pix')
    
    # Get coordinates
    radius, x, y = _coord_circle(image=win, diameter=size, x=x, y=y, method="psychopy")
    
    # Border outline to be same as fill outline colour
    if outline != 0:
        if color_outline == "copy":
            color_outline = color

    # Circle parameters
    circle = visual.Circle(win=win, radius=radius,
                           units="pix", fillColor=color, lineWidth=outline,
                           lineColor=color_outline, edges=radius*2, interpolate=antialias)
    circle.pos = [x-width/2, y-height/2]
    
    
    # blur
    if blur > 0:
        circle.opacity = blur
    
    # Display
    while True:
        circle.draw()
        win.flip()
    
        if 'escape' in event.getKeys():
            win.close()
            core.quit()
