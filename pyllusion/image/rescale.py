# This was copied from NeuroKit2.
import numpy as np


def rescale(x, to=[0, 1], scale=None):
    """Rescale data.

    Rescale a numeric variable to a new range.

    Parameters
    ----------
    x : Union[list, np.array, pd.Series]
        Raw data.
    to : list
        New range of values of x after rescaling.
    scale : list
        A list or tuple of two values specifying the actual range
        of the data. If None, the minimum and the maximum of the
        provided data will be used.

    Returns
    ----------
    list
        The rescaled values.


    Examples
    ----------
    >>> import pyllusion as ill
    >>>
    >>> ill.rescale([3, 1, 2, 4, 6], to=[0, 1]) #doctest: +ELLIPSIS
    [0.4, 0.0, 0.2, 0.6000000000000001, 1.0]

    """

    # Return appropriate type
    if isinstance(x, list):
        x = list(_rescale(np.array(x), to=to, scale=scale))
    else:
        x = _rescale(x, to=to, scale=scale)

    return x


# =============================================================================
# Internals
# =============================================================================
def _rescale(x, to=[0, 1], scale=None):
    if scale is None:
        scale = [np.nanmin(x), np.nanmax(x)]

    return (to[1] - to[0]) / (scale[1] - scale[0]) * (x - scale[0]) + to[0]
