import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from psychopy import visual
from ..image import image_line
from ..image.utilities import _coord_line
from .ponzo import _ponzo_parameters_topbottom


def mullerlyer_psychopy(window, parameters=None, outline=5, **kwargs):

    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event

    >>> parameters = ill.mullerlyer_parameters(difficulty=0, illusion_strength=30)

    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], fullscr=False,
                               screen=0, winType='pyglet', monitor='testMonitor',
                               allowGUI=False, color="white",
                               blendMode='avg', units='pix')
    
    >>> # Display illusion
    >>> ill.mullerlyer_psychopy(window=window, parameters=parameters)
    
    >>> # Refresh and close window    
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()

    """    
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = mullerlyer_parameters(**kwargs)

    # Loop lines
    for which in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:
        # Draw distractor lines
        for side in ["1", "2"]:
            coord, _, _ = _coord_line(image=window,
                                      x1=parameters["Distractor_" + which + side + "_x1"],
                                      y1=parameters["Distractor_" + which + side + "_y1"],
                                      x2=parameters["Distractor_" + which + side + "_x2"],
                                      y2=parameters["Distractor_" + which + side + "_y2"],
                                      method="psychopy")
            # line parameters
            line_distractor = visual.Line(win=window, units='pix',
                                          lineColor="black", lineWidth=outline)
            line_distractor.start = [coord[0]-window.size[0]/2, coord[1]-window.size[1]/2]
            line_distractor.end = [coord[2]-window.size[0]/2, coord[3]-window.size[1]/2]
            line_distractor.draw()
    
    for position in ["Bottom", "Top"]:
        # Draw target lines
        coord, _, _ = _coord_line(image=window,
                                  x1=parameters[position + "_x1"],
                                  y1=parameters[position + "_y1"],
                                  x2=parameters[position + "_x2"],
                                  y2=parameters[position + "_y2"],
                                  method="psychopy")
        # Line parameters
        line_target = visual.Line(win=window, units='pix',
                                  lineColor="red", lineWidth=outline)
        line_target.start = [coord[0]-window.size[0]/2, coord[1]-window.size[1]/2]
        line_target.end = [coord[2]-window.size[0]/2, coord[3]-window.size[1]/2]
        line_target.draw()




def mullerlyer_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):
    """
    Create the Müller-Lyer illusion.
    The Müller-Lyer illusion is an optical illusion causing the participant to
    perceive two segments as being of different length depending on the shape of
    the arrows.
    
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.mullerlyer_parameters(difficulty=0, illusion_strength=3)
    >>> ill.mullerlyer_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    >>> parameters = ill.mullerlyer_parameters(difficulty=0, illusion_strength=30)
    >>> ill.mullerlyer_image(parameters)  #doctest: +ELLIPSIS
    <PIL.Image.Image ...>
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = mullerlyer_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Distractors lines
    for which in ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]:  #
        for side in ["1", "2"]:
            image = image_line(
                image=image,
                x1=parameters["Distractor_" + which + side + "_x1"],
                y1=parameters["Distractor_" + which + side + "_y1"],
                x2=parameters["Distractor_" + which + side + "_x2"],
                y2=parameters["Distractor_" + which + side + "_y2"],
                color="black",
                size=outline)

    # Target lines (horizontal)
    for position in ["Bottom", "Top"]:
        image = image_line(image=image,
                   x1=parameters[position + "_x1"],
                   y1=parameters[position + "_y1"],
                   x2=parameters[position + "_x2"],
                   y2=parameters[position + "_y2"],
                   color="red",
                   size=outline)

    return image



def mullerlyer_parameters(difficulty=0, size_min=0.5, illusion_strength=0, distance=1):
    parameters = _ponzo_parameters_topbottom(difficulty=difficulty, size_min=size_min, distance=distance)

    length = size_min/2

    if difficulty >= 0:
        angle = {"Top": -illusion_strength, "Bottom": illusion_strength}
    else:
        angle = {"Top": illusion_strength, "Bottom": -illusion_strength}

    for which in ["Top", "Bottom"]:
        for side in ["Left", "Right"]:
            if side == "Left":
                coord, _, _ = _coord_line(x1=parameters[which + "_x1"], y1=parameters[which + "_y1"], length=length, angle=angle[which])
            else:
                coord, _, _ = _coord_line(x1=parameters[which + "_x2"], y1=parameters[which + "_y2"], length=length, angle=-angle[which])
            x1, y1, x2, y2 = coord

            for c in ["1", "2"]:
                parameters["Distractor_" + which + side + c + "_x1"] = x1
                parameters["Distractor_" + which + side + c + "_y1"] = y1
                parameters["Distractor_" + which + side + c + "_x2"] = x2
                if c == "1":
                    parameters["Distractor_" + which + side + c + "_y2"] = y2
                else:
                    parameters["Distractor_" + which + side + c + "_y2"] = y2 - 2 * (y2 - y1)


    parameters.update({"Illusion": "MullerLyer",
                       "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
                       "Distractor_Length": length})

    return parameters
  
