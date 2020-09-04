def images_to_gif(images, path="mygif.gif", fps=30):
    """
    >>> import pyllusion as ill
    >>>
    >>> ill.image_blobs(n=500)  #doctest: +ELLIPSIS
     <PIL.Image.Image ...>
    """
    try:
        import imageio
    except ImportError:
        raise ImportError(
            "The 'imageio' module is required for this function to run. ",
            "Please install it by running `pip install imageio`",
        )
    duration = 1 / fps
    imageio.mimsave(path, images, duration=duration, fps=fps)
