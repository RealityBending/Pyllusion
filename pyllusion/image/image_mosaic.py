import numpy as np
import PIL.Image


def image_mosaic(image_list, ncols="auto", nrows="auto"):
    """Collate images together in a mosaic.

    Parameters
    ----------
    image_list : list
        A list of PIL images.
    ncols, nrows : int
        How many rows and columns.

    Returns
    -------
    Image
        A PIL image.

    Examples
    --------
    >>> import pyllusion
    >>>
    >>> img1 = pyllusion.delboeuf_image()
    >>> img2 = pyllusion.ponzo_image()
    >>> img3 = pyllusion.rodframe_image()
    >>> img4 = pyllusion.mullerlyer_image()
    >>> img5 = pyllusion.ebbinghaus_image()
    >>> pyllusion.image_mosaic([img1, img2, img3, img4, img5], ncols=2)
    """
    # Compute dimensions
    n = len(image_list)
    if (n % 2) != 0:  # If Odd number
        n += 1
    if ncols == "auto" and nrows == "auto":
        ncols = int(np.ceil(np.sqrt(n)))
        nrows = int(n / ncols)
    elif ncols == "auto" and nrows != "auto":
        ncols = int(n / nrows)
    elif ncols != "auto" and nrows == "auto":
        nrows = int(n / ncols)

    # Generate image
    new = PIL.Image.new('RGB', (image_list[0].width * ncols, image_list[0].height * nrows))
    i = 0
    for row in range(nrows):
        for col in range(ncols):
            try:
                new.paste(image_list[i], (image_list[i].width * col, image_list[i].height * row))
            except IndexError:
                pass
            i += 1
    return new
