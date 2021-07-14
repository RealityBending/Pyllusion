from .delboeuf_image import _delboeuf_image
from .delboeuf_parameters import _delboeuf_parameters
from .delboeuf_psychopy import _delboeuf_psychopy


class Delboeuf:
    """
    A class to generate a Delboeuf illusion.
    """

    def __init__(
        self, illusion_strength=0, difference=0, size_min=0.25, distance=1, distance_auto=False
    ):
        """
        __init__ Docstrings for _delboeuf_parameters().

        Parameters
        ----------
        illusion_strength : int, optional
            [description], by default 0
        difference : int, optional
            [description], by default 0
        size_min : float, optional
            [description], by default 0.25
        distance : int, optional
            [description], by default 1
        distance_auto : bool, optional
            [description], by default False
        """

        self.parameters = _delboeuf_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            size_min=size_min,
            distance=distance,
            distance_auto=distance_auto,
        )

    def get_parameters(self):
        """
        get_parameters [summary]
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, outline=10, background="white", **kwargs):
        """"""
        img = _delboeuf_image(
            self.parameters,
            width=width,
            height=height,
            outline=outline,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """"""
        _delboeuf_psychopy(self.parameters, window, **kwargs)
