import numpy as np

from ..image import image_circle, image_circles
from .movement_matrix import movement_matrix


def motiontransparency_images(parameters=None, width=800, height=500, **kwargs):
    """
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.motiontransparency_parameters(angle=45, duration=4, n=100, fps=20, speed=2)
    >>> images = ill.motiontransparency_images(parameters)  #doctest: +ELLIPSIS
    - 0.00% ...
    >>> # ill.images_to_gif(images, path="Transparency_From_Motion.gif", fps=parameters["FPS"])
    """
    if parameters is None:
        parameters = motiontransparency_parameters(**kwargs)

    # Adjust for screen ratio
    if width is not None and height is not None:
        parameters["x"] = parameters["x"] * (height / width)

    # Generate PIL images
    images = []
    for i in range(parameters["n_Frames"]):
        # Print progression
        if i % 10 == 0:
            print("- %.2f%%" % (i / parameters["n_Frames"] * 100))

        # Background circle
        image = image_circle(
            width=width,
            height=height,
            size=1,
            color="grey",
            outline=0,
            color_outline="red",
            background=(100, 100, 100),
            antialias=True,
        )

        # Draw points
        image = image_circles(
            image=image,
            n=parameters["n_Points"],
            x=parameters["x"][i],
            y=parameters["y"][i],
            color="black",
            background="grey",
            size=0.015,
            antialias=False,
        )

        images.append(image)

    return images


def motiontransparency_parameters(angle=None, n=200, duration=0.5, fps=60, speed=1):
    """
    """
    n_frames = int(duration * fps)

    if angle is None:
        angle = np.random.uniform(0, 360)
    angles = np.array([angle] * int(n / 2) + [180 + angle] * int(n / 2))

    x, y = movement_matrix(
        n=n,
        n_frames=n_frames,
        angle=angles,
        speed=speed,
        keep_in_window=False,
        keep_in_circle=0.5,
    )

    parameters = {
        "x": x,
        "y": y,
        "Angle": angle,
        "Speed": speed,
        "Duration": duration,
        "FPS": fps,
        "n_Frames": n_frames,
        "n_Points": n,
    }
    return parameters
