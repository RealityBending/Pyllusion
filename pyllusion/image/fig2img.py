import io

import PIL.Image


def fig2img(fig):
    """Matplotlib Figure to PIL Image

    Convert a Matplotlib figure to a PIL Image

    Parameters
    ----------
    fig : plt.figure
        Matplotlib figure.

    Returns
    ----------
    list
        The rescaled values.


    Examples
    ----------
    >>> import pyllusion
    >>> import matplotlib.pyplot as plt
    >>>
    >>> plt.plot([1, 2, 3, 4, 5])
    >>> fig = plt.gcf()
    >>> pyllusion.fig2img(fig)

    """
    buffer = io.BytesIO()
    fig.savefig(buffer)
    buffer.seek(0)
    img = PIL.Image.open(buffer)
    return img