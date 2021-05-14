import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line
from ..image.utilities import _coord_line
from ..psychopy import psychopy_line


def zollner_psychopy(window, parameters=None, **kwargs):
    """Create a PsychoPy stimulus of the Zöllner illusion.
    
    
    The Zöllner illusion is an optical illusion, where horizontal lines are perceived
    as not parallel because of their background.

    Parameters
    ----------
    window : object
        The window object in which the stimulus will be rendered.
    parameters : dict
        Parameters of the Zöllner illusion generated by `zollner_parameters()`.
    **kwargs
        Additional arguments passed into `zollner_parameters()`.
    
    Returns
    -------
    In-place modification of the PsychoPy window (No explicit return).


    Examples
    ---------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event

    >>> # Create parameters
    >>> parameters = ill.zollner_parameters(illusion_strength=75)

    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], winType='pyglet', color='white')
    
    >>> # Display illusion
    >>> ill.zollner_psychopy(window=window, parameters=parameters)
    
    >>> # Refresh and close window    
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()

    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = zollner_parameters(**kwargs)

    # Loop lines
    for i in range(parameters["Distractors_n"]):
        # Draw distractor lines
        for pos in ["_Top_", "_Bottom_"]:
            psychopy_line(window,
                          x1=parameters["Distractors" + pos + "x1"][i],
                          y1=parameters["Distractors" + pos + "y1"][i],
                          x2=parameters["Distractors" + pos + "x2"][i],
                          y2=parameters["Distractors" + pos + "y2"][i],
                          adjust_height=True,
                          color="black", size=5)
    
    for pos in ["Bottom", "Top"]:
        # Draw target lines
        psychopy_line(window,
                      x1=parameters[pos + "_x1"],
                      y1=parameters[pos + "_y1"],
                      x2=parameters[pos + "_x2"],
                      y2=parameters[pos + "_y2"],
                      adjust_height=True,
                      color="red", size=5)
        

def zollner_image(parameters=None, width=800, height=600, background="white", **kwargs):
    """Create a PIL image of the Zöllner illusion.
    
    
    The Zöllner illusion is an optical illusion, where horizontal lines are perceived
    as not parallel because of their background.

    Parameters
    ----------
    parameters : dict
        Parameters of the Zöllner illusion generated by `zollner_parameters()`.
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    background : str
        Color of the background.
    **kwargs
        Additional arguments passed into `zollner_parameters()`.

    Returns
    -------
    Image
        Image of the Zöllner illusion, defaults to 800 x 600 pixels.
        Can be resized
        (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
        and saved in different file formats
        (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.zollner_parameters(illusion_strength=75)
    >>> ill.zollner_image(parameters)
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = zollner_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Lines
    for pos in ["Top_", "Bottom_"]:
        image = image_line(
            image=image,
            x1=parameters[pos + "x1"],
            y1=parameters[pos + "y1"],
            x2=parameters[pos + "x2"],
            y2=parameters[pos + "y2"],
            color="red",
            adjust_height=True,
            size=20,
        )

    # Distractors
    for i in range(parameters["Distractors_n"]):
        for pos in ["_Top_", "_Bottom_"]:
            image = image_line(
                image=image,
                x1=parameters["Distractors" + pos + "x1"][i],
                y1=parameters["Distractors" + pos + "y1"][i],
                x2=parameters["Distractors" + pos + "x2"][i],
                y2=parameters["Distractors" + pos + "y2"][i],
                color="black",
                adjust_height=True,
                size=20,
            )

    return image


def zollner_parameters(
    illusion_strength=0, difference=0, distractors_n=8, distractors_length=0.66
):
    """Compute Parameters for Zöllner illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the background, i.e., tilted distractor lines, in biasing the perception of unparallel horizontal lines.
        Specifically, the angle of the distractor lines in degrees, where larger values represent less
        steep distractor lines and greater susceptibiltiy to the illusion. A negative sign
        flips the perceived conversion direction of the illusion.
    difference : float
        The objective parallel alignment of the two horizontal lines. 
        Specifically, the angle of the two horizontal target lines in degrees, where ``difference=10`` represents
        a 10 degree tilt of the lines towards each other. A negative sign
        flips the perceived conversion direction of the illusion.
    distractors_n : int
        Number of distractor lines in the background.
    distractors_length : float
        Length of distractor lines in the background.
    
    Returns
    -------
    dict
        Dictionary of parameters of the Zöllner illusion.

    """

    # Coordinates of target lines
    coord, _, _ = _coord_line(y=0.33, length=10, angle=90 + difference)
    top_x1, top_y1, top_x2, top_y2 = coord
    coord, _, _ = _coord_line(y=-0.33, length=10, angle=90 - difference)
    bottom_x1, bottom_y1, bottom_x2, bottom_y2 = coord

    # Angle distractors
    if difference >= 0:
        angle = illusion_strength + difference
    else:
        angle = -illusion_strength + difference

    # Get slope of lines to be able to place the distractors on them
    slope_top = (top_y2 - top_y1) / (top_x2 - top_x1)
    slope_bottom = (bottom_y2 - bottom_y1) / (bottom_x2 - bottom_x1)

    # Coordinate of distractors
    distractors_top_x1 = np.zeros(distractors_n)
    distractors_top_y1 = np.zeros(distractors_n)
    distractors_top_x2 = np.zeros(distractors_n)
    distractors_top_y2 = np.zeros(distractors_n)
    distractors_bottom_x1 = np.zeros(distractors_n)
    distractors_bottom_y1 = np.zeros(distractors_n)
    distractors_bottom_x2 = np.zeros(distractors_n)
    distractors_bottom_y2 = np.zeros(distractors_n)
    for i, x in enumerate(np.linspace(-0.9, 0.9, num=distractors_n)):
        coord, _, _ = _coord_line(
            y=0.33 + x * slope_top, x=x, length=distractors_length, angle=angle,
        )
        x1, y1, x2, y2 = coord
        distractors_top_x1[i] = x1
        distractors_top_y1[i] = y1
        distractors_top_x2[i] = x2
        distractors_top_y2[i] = y2

        coord, _, _ = _coord_line(
            y=-0.33 + x * slope_bottom, x=x, length=distractors_length, angle=-angle,
        )
        x1, y1, x2, y2 = coord
        distractors_bottom_x1[i] = x1
        distractors_bottom_y1[i] = y1
        distractors_bottom_x2[i] = x2
        distractors_bottom_y2[i] = y2

    parameters = {
        "Illusion": "Zollner",
        "Illusion_Strength": illusion_strength,
        "Difference": difference,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Top_x1": top_x1,
        "Top_y1": top_y1,
        "Top_x2": top_x2,
        "Top_y2": top_y2,
        "Bottom_x1": bottom_x1,
        "Bottom_y1": bottom_y1,
        "Bottom_x2": bottom_x2,
        "Bottom_y2": bottom_y2,
        "Distractors_n": distractors_n,
        "Distractors_Top_x1": distractors_top_x1,
        "Distractors_Top_y1": distractors_top_y1,
        "Distractors_Top_x2": distractors_top_x2,
        "Distractors_Top_y2": distractors_top_y2,
        "Distractors_Bottom_x1": distractors_bottom_x1,
        "Distractors_Bottom_y1": distractors_bottom_y1,
        "Distractors_Bottom_x2": distractors_bottom_x2,
        "Distractors_Bottom_y2": distractors_bottom_y2,
        "Distractors_Angle": angle,
    }

    return parameters
