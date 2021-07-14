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

    def update(self, illusion_strength=None, difference=None, size_min=None,
               distance=None, distance_auto=None):
        """
        update [summary]

        Parameters
        ----------
        parameters : [type]
            [description]
        """
        # Try loading inspect
        try:
            import inspect
        except ImportError:
            raise ImportError(
                "Pyllusion error: update(): the 'inspect' module is required for this function to run. ",
                "Please install it first (`pip install inspect`).",
            )

        # get original values
        values = inspect.getfullargspec(self.__init__)[3]

        if illusion_strength is None:
            illusion_strength = values[0]
        if difference is None:
            difference = values[1]
        if size_min is None:
            size_min = values[2]
        if distance is None:
            distance = values[3]
        if distance_auto is None:
            distance_auto = values[4]

        self.parameters = _delboeuf_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            size_min=size_min,
            distance=distance,
            distance_auto=distance_auto,
        )
        # self.parameters.update(parameters)

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
            parameters=self.parameters,
            width=width,
            height=height,
            outline=outline,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """"""
        _delboeuf_psychopy(window, self.parameters, **kwargs)
