import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from ..image import image_line, image_rectangle
from ..image.utilities import _coord_line

def rodframe_image(parameters=None, width=800, height=600, outline=20, background="white", **kwargs):
    """
    Examples
    ---------
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.rodframe_parameters(difficulty=0, illusion_strength=11)
    >>> ill.rodframe_image(parameters)

    """
    # Create white canvas and get drawing context
    if parameters is None:
        parameters = rodframe_parameters(**kwargs)

    # Background
    image  = PIL.Image.new('RGB', (width, height), color=background)

    # Frame
    image = image_rectangle(
        image=image,
        size_width=1,
        size_height=1,
        rotate=parameters["Frame_Angle"],
        color=(0, 0, 0, 0),
        outline=20,
        adjust_width=True)

    # Rod
    coord, _, _ = _coord_line(x1=0, y1=0, length=0.4, angle=parameters["Rod_Angle"])
    _, _, x2, y2 = coord
    coord, _, _ = _coord_line(x1=0, y1=0, length=0.4, angle=180+parameters["Rod_Angle"])
    _, _, x1, y1 = coord

    image = image_line(
        image=image,
        x=x1,
        y=y1,
        x2=x2,
        y2=y2,
        length=None,
        rotate=None,
        color="red",
        size=20)

    return image



def rodframe_parameters(difficulty=0, illusion_strength=0):
    """
    Rod and Frame Illusion

    Parameters
    ----------
    difficulty : float
        Rod Angle (clockwise).
    illusion : float
        Frame Angle (clockwise).
    """
    rod_angle = difficulty

    if difficulty >= 0:
        frame_angle = illusion_strength
    else:
        frame_angle = -1 * illusion_strength




    parameters = {"Frame_Angle": frame_angle,
                  "Rod_Angle": rod_angle,
                  "Angle_Difference": rod_angle - frame_angle,
                  "Difficulty": rod_angle,
                  "Illusion": illusion_strength,
                  "Illusion_Type": "Congruent" if illusion_strength > 0 else "Incongruent"
                  }

    return parameters
