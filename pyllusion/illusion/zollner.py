import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from psychopy import visual, event
from ..image import image_line
from ..image.utilities import _coord_line


def zollner_psychopy(window, parameters=None, outline=5, **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event

    >>> parameters = ill.zollner_parameters(illusion_strength=75)

    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], fullscr=False,
                               screen=0, winType='pyglet', monitor='testMonitor',
                               allowGUI=False, color="white",
                               blendMode='avg', units='pix')
    
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
            coord, _, _ = _coord_line(image=window,
                                      x1=parameters["Distractors" + pos + "x1"][i],
                                      y1=parameters["Distractors" + pos + "y1"][i],
                                      x2=parameters["Distractors" + pos + "x2"][i],
                                      y2=parameters["Distractors" + pos + "y2"][i],
                                      adjust_height=True,
                                      method="psychopy")

            # line parameters
            line_distractor = visual.Line(win=window, units='pix',
                                          lineColor="black", lineWidth=outline)
            line_distractor.start = [coord[0]-window.size[0]/2, coord[1]-window.size[1]/2]
            line_distractor.end = [coord[2]-window.size[0]/2, coord[3]-window.size[1]/2]
            line_distractor.draw()
    
    for pos in ["Bottom", "Top"]:
        # Draw target lines
        coord, _, _ = _coord_line(image=window,
                                  x1=parameters[pos + "_x1"],
                                  y1=parameters[pos + "_y1"],
                                  x2=parameters[pos + "_x2"],
                                  y2=parameters[pos + "_y2"],
                                  adjust_height=True,
                                  method="psychopy")
        # Line parameters
        line_target = visual.Line(win=window, units='pix',
                                  lineColor="red", lineWidth=outline)
        line_target.start = [coord[0]-window.size[0]/2, coord[1]-window.size[1]/2]
        line_target.end = [coord[2]-window.size[0]/2, coord[3]-window.size[1]/2]
        line_target.draw()
    


    
    
def zollner_image(parameters=None, width=800, height=600, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.zollner_parameters(illusion_strength=75)
    >>> ill.zollner_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
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
    difference=0, illusion_strength=0, distractors_n=8, distractors_length=0.66
):
    """
    Zollner Illusion

    Parameters
    ----------
    difficulty : float
        Top line angle (clockwise).
    illusion : float
        Top distractor lines angle (clockwise).
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
