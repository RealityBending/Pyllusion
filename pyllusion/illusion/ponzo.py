import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line
from ..image.utilities import _coord_line
from ..psychopy import psychopy_line


def ponzo_psychopy(window, parameters=None, **kwargs):
    """Create a PsychoPy stimulus of the Ponzo illusion.
    
    
    The Ponzo illusion is an optical illusion of relative size perception, where
    horizontal lines of identical size appear as different because of their surrounding context.
    
    Parameters
    ----------
    window : object
        The window object in which the stimulus will be rendered.
    parameters : dict
        Parameters of the Ponzo illusion generated by `ponzo_parameters()`.
    **kwargs
        Additional arguments passed into `ponzo_parameters()`.
    
    Returns
    -------
    In-place modification of the PsychoPy window (No explicit return).

    Examples
    ---------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event

    >>> # Create parameters
    >>> parameters = ill.ponzo_parameters(illusion_strength=20)

    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], winType='pygame', color="white")
    
    >>> # Display illusion
    >>> ill.ponzo_psychopy(window=window, parameters=parameters)
    
    >>> # Refresh and close window    
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()

    """    
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = ponzo_parameters(**kwargs)

    # Loop lines
    for side in ["Left", "Right"]:
        # Draw distractor lines
        psychopy_line(window,
                      x1=parameters[side + "_x1"],
                      y1=parameters[side + "_y1"],
                      x2=parameters[side + "_x2"],
                      y2=parameters[side + "_y2"],
                      color="black", size=5)

    for position in ["Bottom", "Top"]:
        # Draw target lines
        psychopy_line(window,
                      x1=parameters[position + "_x1"],
                      y1=parameters[position + "_y1"],
                      x2=parameters[position + "_x2"],
                      y2=parameters[position + "_y2"],
                      color="red", size=5)

    
def ponzo_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):
    """Create a PIL image of the Ponzo illusion.
    
    
    The Ponzo illusion is an optical illusion of relative size perception, where
    horizontal lines of identical size appear as different because of their surrounding context.

    Parameters
    ----------
    parameters : dict
        Parameters of the Ponzo illusion generated by `ponzo_parameters()`.
    width : int
        Width of the returned image.
    height : int
        Height of the returned image.
    outline : float
        The width of the lines in the illusion, passed into `image_line()`.        
    background : str
        Color of the background.
    **kwargs
        Additional arguments passed into `ponzo_parameters()`.

    Returns
    -------
    Image
        Image of the Ponzo illusion, defaults to 800 x 600 pixels.
        Can be resized
        (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
        and saved in different file formats
        (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.ponzo_parameters(illusion_strength=20)
    >>> ill.ponzo_image(parameters)
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = ponzo_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Distractors lines
    for side in ["Left", "Right"]:
        image = image_line(
            image=image,
            x1=parameters[side + "_x1"],
            y1=parameters[side + "_y1"],
            x2=parameters[side + "_x2"],
            y2=parameters[side + "_y2"],
            color="black",
            size=outline,
        )

    # Target lines (horizontal)
    for position in ["Bottom", "Top"]:
        image = image_line(
            image=image,
            x1=parameters[position + "_x1"],
            y1=parameters[position + "_y1"],
            x2=parameters[position + "_x2"],
            y2=parameters[position + "_y2"],
            color="red",
            size=outline,
        )

    return image


# ------------------------------------------
# Parameters
# ------------------------------------------


def ponzo_parameters(illusion_strength=0, difference=0, size_min=0.5, distance=1):
    """Compute Parameters for Ponzo Illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the tilting vertical lines in biasing the perception of horizontal lines of unequal lengths.
        Specifically, the angle of the vertical lines in degrees, i.e., ``illusion_strength=20`` represents
        a 20 degree tilt of the vertical lines converging at the top. A negative sign
        represents vertical lines converging at the bottom.
    difference : float
        The objective length difference of the two horizontal lines.
        Specifically, the real difference of the upper horizontal line relative to the lower horizontal line. E.g.,
        if ``difference=1``, the upper line will be 100% longer, i.e., 2 times longer than
        the lower line. A negative sign reflects the converse, where ``difference=-1``
        will result in the lower line being 100% longer than the upper line.        
    size_min : float
        Length of lower horizontal line.
    distance : float
        Distance between the upper and lower horizontal lines.

    Returns
    -------
    dict
        Dictionary of parameters of the Ponzo illusion.
    """
    parameters = _ponzo_parameters_topbottom(
        difference=difference, size_min=size_min, distance=distance
    )

    parameters.update(_ponzo_parameters_leftright(difference, illusion_strength))

    parameters.update({"Illusion": "Ponzo"})

    return parameters


def _ponzo_parameters_leftright(difference, illusion_strength):
    # Angle of lines
    angle = illusion_strength
    angle = -1 * angle if difference > 0 else angle

    # Left line
    left_coord, length, _ = _coord_line(x=-0.5, y=0, length=1, angle=angle)
    left_x1, left_y1, left_x2, left_y2, length = _ponzo_parameters_adjust(
        left_coord, angle, side="Left"
    )

    # Right line
    right_coord, length, _ = _coord_line(x=0.5, y=0, length=1, angle=-angle)
    right_x1, right_y1, right_x2, right_y2, length = _ponzo_parameters_adjust(
        right_coord, angle, side="Right"
    )

    parameters = {
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",
        "Side_Angle": angle,
        "Side_Length": length,
        "Left_x1": left_x1,
        "Left_y1": left_y1,
        "Left_x2": left_x2,
        "Left_y2": left_y2,
        "Right_x1": right_x1,
        "Right_y1": right_y1,
        "Right_x2": right_x2,
        "Right_y2": right_y2,
    }
    return parameters


def _ponzo_parameters_adjust(coord, angle, side="Left"):
    # Modify upper and lower points
    if side == "Left":
        x1, y1, x2, y2 = coord

        # Fix upper y to 0.5
        y2 = 1.1
        x2 = (y2 - y1) * np.tan(np.deg2rad(angle)) + x1
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Fix lower y to -0.5
        y1 = -1.1
        x1 = -1 * ((y2 - y1) * np.tan(np.deg2rad(angle)) - x2)
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        x1, y1, x2, y2 = coord

        # Fix upper y to 0.5
        y2 = 1.1
        x2 = -1 * ((y2 - y1) * np.tan(np.deg2rad(angle)) - x1)
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        # Fix lower y to -0.5
        y1 = -1.1
        x1 = (y2 - y1) * np.tan(np.deg2rad(angle)) + x2
        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Prevent clipping
    if side == "Left":
        if x2 > 0:
            x2 = 0
            y2 = (x2 - x1) * np.tan(np.deg2rad(90 - angle)) + y1
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if x1 > 0:
            x1 = 0
            y1 = -1 * ((x2 - x1) * np.tan(np.deg2rad(90 - angle)) - y2)
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        if x2 < 0:
            x2 = 0
            y2 = -1 * ((x2 - x1) * np.tan(np.deg2rad(90 - angle)) - y1)
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if x1 < 0:
            x1 = 0
            y1 = (x2 - x1) * np.tan(np.deg2rad(90 - angle)) + y2
            length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return x1, y1, x2, y2, length


def _ponzo_parameters_topbottom(difference=0, size_min=0.5, distance=1):

    if difference > 0:  # if down is smaller
        bottom_length = size_min
        top_length = (1 + np.abs(difference)) * size_min
    else:
        top_length = size_min
        bottom_length = (1 + np.abs(difference)) * size_min

    bottom_x1 = -(bottom_length / 2)
    bottom_y1 = -(distance / 2)
    bottom_x2 = bottom_length / 2
    bottom_y2 = -(distance / 2)

    top_x1 = -(top_length / 2)
    top_y1 = distance / 2
    top_x2 = top_length / 2
    top_y2 = distance / 2

    parameters = {
        "Difference": difference,
        "Distance": distance,
        "Bottom_x1": bottom_x1,
        "Bottom_y1": bottom_y1,
        "Bottom_x2": bottom_x2,
        "Bottom_y2": bottom_y2,
        "Top_x1": top_x1,
        "Top_y1": top_y1,
        "Top_x2": top_x2,
        "Top_y2": top_y2,
        "Size_Bottom": bottom_length,
        "Size_Top": top_length,
        "Size_Larger": np.max([top_length, bottom_length]),
        "Size_Smaller": np.min([top_length, bottom_length]),
    }

    return parameters
