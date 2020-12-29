import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from psychopy import visual
from ..image import image_circle
from ..image.utilities import _coord_circle


def delboeuf_psychopy(window, parameters=None, **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>> from psychopy import visual, event
    
    >>> parameters = ill.delboeuf_parameters(difficulty=2, illusion_strength=1)
    
    >>> # Initiate Window
    >>> window = visual.Window(size=[800, 600], fullscr=False,
                               screen=0, winType='pyglet', monitor='testMonitor',
                               allowGUI=False, color="white",
                               blendMode='avg', units='pix')
    
    >>> # Display illusion
    >>> ill.delboeuf_psychopy(window=window, parameters=parameters)
    
    >>> # Refresh and close window    
    >>> window.flip()
    >>> event.waitKeys()  # Press any key to close
    >>> window.close()
    """

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = delboeuf_parameters(**kwargs)

    # Loop circles 
    for side in ["Left", "Right"]:
        # Draw outer circle
        radius_outer, x_outer, y_outer = _coord_circle(image=window,
                                                       diameter=parameters["Size_Outer_" + side],
                                                       x=parameters["Position_" + side],
                                                       y=0, method="psychopy")
        circle_outer = visual.Circle(win=window, units="pix", fillColor="white",
                                     lineColor="black", edges=128,
                                     radius=radius_outer, lineWidth=3)  # linewidth fixed
        circle_outer.pos = [x_outer-window.size[0]/2, y_outer-window.size[1]/2]
        circle_outer.draw()
        
        # Draw inner circle
        radius_inner, x_inner, y_inner = _coord_circle(image=window,
                                                       diameter=parameters["Size_Inner_" + side],
                                                       x=parameters["Position_" + side],
                                                       y=0, method="psychopy")
        circle_inner = visual.Circle(win=window, units="pix", fillColor="red",
                                     lineColor="red", edges=128,
                                     radius=radius_inner, lineWidth=0.5)
        circle_inner.pos = [x_inner-window.size[0]/2, y_inner-window.size[1]/2]
        circle_inner.draw()
        


def delboeuf_image(parameters=None, width=800, height=600, outline=10,
                   background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.delboeuf_parameters(difficulty=2, illusion_strength=1)
    >>> ill.delboeuf_image(parameters)  #doctest: +ELLIPSIS
    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = delboeuf_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Outer circles (outlines)
    image = image_circle(image=image,
                         x=parameters["Position_Left"],
                         size=parameters["Size_Outer_Left"],
                         color=(0, 0, 0, 0),
                         outline=outline)
    image = image_circle(image=image,
                         x=parameters["Position_Right"],
                         size=parameters["Size_Outer_Right"],
                         color=(0, 0, 0, 0),
                         outline=outline)

    # Inner circles
    image = image_circle(image=image,
                         x=parameters["Position_Left"],
                         size=parameters["Size_Inner_Left"],
                         color="red")
    image = image_circle(image=image,
                         x=parameters["Position_Right"],
                         size=parameters["Size_Inner_Right"],
                         color="red")
    
    return image



# ------------------------------------------
# Parameters
# ------------------------------------------

def delboeuf_parameters(difficulty=0, size_min=0.25, illusion_strength=0, distance=1, distance_auto=False):
    """Compute Parameters for Delboeuf Illusion.

    Parameters
    ----------
    difficulty : float
        Size of left inner circle as relative to the right (in percentage, e.g., if ``difficulty=1``,
        it means that the left circle will be 100% bigger, i.e., 2 times bigger than the right).
    size_min : float
        Size of smaller inner circle.
    illusion : float
        Size of outer circles.
    distance : float
        distance between circles.
    distance_auto : bool
        If true, distance is between edges (fixed spacing), if false, between centers (fixed location).

    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.delboeuf_parameters()
    """
    # Size inner circles
    parameters = _delboeuf_parameters_sizeinner(difficulty=difficulty, size_min=size_min)
    inner_size_left = parameters["Size_Inner_Left"]
    inner_size_right = parameters["Size_Inner_Right"]

    # Base size outer circles
    outer_size_left = inner_size_left + (0.2 * size_min)
    outer_size_right = inner_size_right + (0.2 * size_min)

    # Actual outer size based on illusion
    outer_size_left, outer_size_right = _delboeuf_parameters_sizeouter(outer_size_left,
                                                                       outer_size_right,
                                                                       difficulty=difficulty,
                                                                       illusion_strength=illusion_strength)

    # Get location and distances
    if distance_auto is False:
        distance_centers = distance
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)
        distance_edges_inner = distance_centers - (inner_size_left/2 + inner_size_right/2)
        distance_edges_outer = distance_centers - (outer_size_left/2 + outer_size_right/2)
    else:
        distance_edges_outer = distance
        distance_centers = distance_edges_outer + (inner_size_left/2 + inner_size_right/2)
        distance_edges_inner = distance_centers - (outer_size_left/2 + outer_size_right/2)
        position_left, position_right = -(distance_centers / 2), (distance_centers / 2)



    parameters.update({
        "Illusion": "Delboeuf",
        "Illusion_Strength": illusion_strength,
        "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent",

        "Size_Outer_Left": outer_size_left,
        "Size_Outer_Right": outer_size_right,

        "Distance_Centers": distance_centers,
        "Distance_Edges_Inner": distance_edges_inner,
        "Distance_Edges_Outer": distance_edges_outer,

        "Size_Inner_Smaller": np.min([inner_size_left, inner_size_right]),
        "Size_Inner_Larger": np.max([inner_size_left, inner_size_right]),
        "Size_Outer_Smaller": np.min([outer_size_left, outer_size_right]),
        "Size_Outer_Larger": np.max([outer_size_left, outer_size_right]),

        "Position_Left": position_left,
        "Position_Right": position_right
        })

    return parameters


# ------------------------------------------
# Utilities
# ------------------------------------------


def _delboeuf_parameters_sizeouter(outer_size_left, outer_size_right, illusion_strength=0, difficulty=0, both_sizes=False):
    if both_sizes is True:
        illusion_strength = illusion_strength / 2

    # Actual outer size based on illusion
    if difficulty > 0: # if right is smaller
        if illusion_strength > 0:
            outer_size_left = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / np.sqrt(1 + np.abs(illusion_strength))
        else:
            outer_size_right = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / np.sqrt(1 + np.abs(illusion_strength))

    else:
        if illusion_strength > 0:
            outer_size_right = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_right
            if both_sizes is True:
                outer_size_left = outer_size_left / np.sqrt(1 + np.abs(illusion_strength))
        else:
            outer_size_left = np.sqrt(1 + np.abs(illusion_strength)) * outer_size_left
            if both_sizes is True:
                outer_size_right = outer_size_right / np.sqrt(1 + np.abs(illusion_strength))

    return outer_size_left, outer_size_right


def _delboeuf_parameters_sizeinner(difficulty=0, size_min=0.25):

    size_bigger = np.sqrt(1 + np.abs(difficulty)) * size_min

    if difficulty > 0: # if right is smaller
        inner_size_right = size_min
        inner_size_left = size_bigger
    else:
        inner_size_right = size_bigger
        inner_size_left = size_min

    parameters = {"Difficulty": difficulty,
                  "Size_Inner_Left": inner_size_left,
                  "Size_Inner_Right": inner_size_right,
                  "Size_Inner_Difference": np.pi * (size_bigger / 2)**2 / np.pi * (size_min / 2)**2
    }
    return parameters
