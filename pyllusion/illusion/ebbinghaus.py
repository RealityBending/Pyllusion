import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps
from .delboeuf import _delboeuf_parameters_sizeinner


def ebbinghaus_parameters(difference=0, size_min=0.25):
    parameters = _delboeuf_parameters_sizeinner(difference=difference, size_min=size_min)
    inner_size_left = parameters["Size_Inner_Left"]
    inner_size_right = parameters["Size_Inner_Right"]

    return parameters


# params = ebbinghaus_parameters(difference=3)


# width=800; height=600; background="white"
# image  = PIL.Image.new('RGBA', (width, height), color = background)

# image = _ebbinghaus_drawpart(image, x=0, y=0, size_inner=0.25, size_outer=0.10, color_inner="red", color_outer="black")

# image



def _ebbinghaus_drawpart(image, x=0, y=0, size_inner=0.25, size_outer=0.3, color_inner="red", color_outer="black", n="auto"):

    # Draw inner circle
    image = ill.image_circle(image=image, size=size_inner, x=x, y=y, color=color_inner)

    # Get outer circles positions
    outer_x, outer_y = _ebbinghaus_parameters_outercircles(image, x=x, y=y, size_inner=size_inner, size_outer=size_outer, n=n)
    n = len(outer_x)
    for i in range(n):
        image = ill.image_circle(image=image, size=size_outer, x=outer_x[i], y=outer_y[i], color=color_outer)

    return image


def _ebbinghaus_parameters_outercircles(image, x=0, y=0, size_inner=0.25, size_outer=0.3, n="auto"):
    # Get width/height ratio to have equidistant circles
    ratio = image.size[0] / image.size[1]

    # Find distance between center of inner circle and centers of outer circles
    distance = (size_inner / 2) + (size_outer / 2) + 0.01

    # Find n
    if n == "auto":
        perimeter = 2 * np.pi * distance
        n = np.int(perimeter / size_outer)

    # Get position of outer circles
    angle = np.deg2rad(np.linspace(0, 360, num=n, endpoint=False))
    circle_x = x + (np.cos(angle) * distance)
    circle_x = circle_x / ratio  # Adjust for non-squared screen
    circle_y = y + (np.sin(angle) * distance)

    return circle_x, circle_y


