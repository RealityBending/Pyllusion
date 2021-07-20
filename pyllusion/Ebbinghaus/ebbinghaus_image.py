import numpy as np
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import PIL.ImageOps

from ..image import image_circle
from .ebbinghaus_parameters import _ebbinghaus_parameters


def _ebbinghaus_image(
    parameters=None, width=800, height=600, background="white", **kwargs
):

    # Create white canvas and get drawing context
    if parameters is None:
        parameters = _ebbinghaus_parameters(**kwargs)

    # Background
    image = PIL.Image.new("RGB", (width, height), color=background)

    # Outer circles
    for side in ["Left", "Right"]:
        image = _ebbinghaus_image_draw(image,
                                       parameters,
                                       side=side,
                                       color_inner="red",
                                       color_outer="black")

    return image

def _ebbinghaus_image_draw(image, p, side="Left", color_inner="red", color_outer="black"):

    # Draw inner circle
    image = image_circle(image=image, size=p["Size_Inner_" + side], x=p["Position_" + side], y=0, color=color_inner)

    # Get width/height ratio to have equidistant circles
    ratio = image.size[0] / image.size[1]

    # Adjust for non-squared screen
    x = p["Position_Outer_x_" + side] / ratio
    x = x + (p["Position_" + side] - np.mean(x))

    # Plot each outer circles
    for i in range(len(p["Position_Outer_x_" + side])):
        image = image_circle(image=image, size=p["Size_Outer_" + side], x=x[i], y=p["Position_Outer_y_" + side][i], color=color_outer)

    return image
