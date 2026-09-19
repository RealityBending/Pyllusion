def images_to_gif(images, path="mygif.gif", fps=30):
    """Save a list of PIL images as an animated GIF.

    >>> import pyllusion
    >>>
    >>> images = pyllusion.movement_circles(n=50, duration=2, fps=30)
    >>> # pyllusion.images_to_gif(images, path="mygif.gif", fps=30)
    """
    try:
        import imageio
    except ImportError:
        raise ImportError(
            "The 'imageio' module is required for this function to run. ",
            "Please install it by running `pip install imageio`",
        )
    # imageio expects the duration of each frame in milliseconds
    duration = 1000 / fps
    imageio.mimsave(path, images, duration=duration)
