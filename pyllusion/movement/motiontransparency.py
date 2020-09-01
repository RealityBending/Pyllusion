import numpy as np
from .movement_matrix import movement_matrix
from ..image import image_circles, image_circle


def motiontransparency_images(parameters=None, **kwargs):
    """
    >>> import pyllusion as ill
    >>>
    >>> parameters = ill.motiontransparency_parameters(angle=45, duration=4, n=10, fps=10)
    >>> images = ill.motiontransparency_images(parameters)
    >>> ill.images_to_gif(images, path="Transparency_From_Motion.gif", fps=parameters["FPS"])
    """
    if parameters is None:
        motiontransparency_parameters(**kwargs)

    # Generate PIL images
    images = []
    for i in range(parameters["n_Frames"]):
        if i % 10 == 0:
            print("- %.2f%%" % (i / parameters["n_Frames"] * 100))
        image = image_circle(
            color="grey",
            outline=3,
            color_outline="red",
            background="grey",
            antialias=True,
        )

        image = image_circles(
            image=image,
            n=parameters["n_Points"],
            x=parameters["x"][i],
            y=parameters["y"][i],
            color="black",
            background="grey",
            size=0.01,
        )

        images.append(image)

    return images


def motiontransparency_parameters(angle=None, n=200, duration=0.5, fps=60, speed=1):
    """
    """
    n_frames = int(duration * fps)

    if angle is None:
        angle = np.random.uniform(0, 360)
    angles = np.array([angle] * int(n / 2) + [-angle] * int(n / 2))
    x, y = movement_matrix(
        n=n,
        n_frames=n_frames,
        angle=angles,
        speed=speed,
        keep_in_window=False,
        keep_in_circle=1,
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
