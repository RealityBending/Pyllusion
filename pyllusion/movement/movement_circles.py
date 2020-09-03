import numpy as np
from .movement_matrix import movement_matrix
from ..image import image_circles


def movement_circles(n=50, duration=2, fps=30, width=500, height=500, **kwargs):
    """
    >>> import pyllusion as ill
    >>>
    >>> images = ill.movement_circles(n=50, duration=4, fps=30, color="black", size=0.05)
    >>> #ill.images_to_gif(images, path="mygif.gif", fps=30)
    """
    n_frames = int(duration * fps)

    x, y = movement_matrix(n_frames=n_frames, **kwargs)

    # Generate PIL images
    images = []
    for i in range(n_frames):
        images.append(
            image_circles(width=width, height=height, n=n, x=x[i], y=y[i], **kwargs)
        )

    return images
