from .delboeuf_image import _delboeuf_image
from .delboeuf_parameters import _delboeuf_parameters
from .delboeuf_psychopy import _delboeuf_psychopy


class Delboeuf:
    """
    A class to generate the Delboeuf Illusion.

    The Delboeuf illusion is an optical illusion of relative size perception,
    where circles of identical size appear as different because of their surrounding context.
    
    Each instance of ``Delboeuf`` contains attributes corresponding to the parameters of the illusion.
    These parameters are:
        * ``Difference``: Objective difference in the target features, by modifying ``difference`` of ``delboeuf_parameters()``
        * ``Illusion``: Name of the illusion.
        * ``Illusion_Strength``: Strength of the surrounding context in biasing illusion, by modifying ``illusion_strength`` of ``delboeuf_parameters()``.
        * ``Illusion_Type``: 'Congruent' if biased towards perceiving the illusion, and 'Incongruent' if against. 
        * ``Size_Min``: size of the smaller inner circle, by modifying ``size_min`` of ``delboeuf_parameters()``.
        * ``Size_Inner_Left``: Size of the inner left circle.
        * ``Size_Inner_Right``: Size of the inner right circle.
        * ``Sine_Inner_Difference``: Difference in size (area) of the left and right inner circles.
        * ``Size_Outer_Left``: Size of the outer left rim.
        * ``Size_Outer_Right``: Size of the outer right rim.
        * ``Distance``: Distance between the circles, by modifying ``distance`` of ``delboeuf_parameters()``.
        * ``Distance_Reference``: Distance between circles is computed 'Between Edges' or 'Between Centers', by modifying ``distance_auto`` of ``delboeuf_parameters()``.
        * ``Distance_Edges_Inner``: Distance between the edges of the inner left and right circles.
        * ``Distance_Edges_Outer``: Distance between the edges of the outer left and right rims.
        * ``Size_Inner_Smaller``: Size of the smaller inner circle.
        * ``Size_Inner_Larger``: Size of the larger inner circle.
        * ``Size_Outer_Smaller``: Size of the smaller outer rim.
        * ``Size_Outer_Larger``: Size of the larger outer rim.
        * ``Position_Left``: Position of the left circle.
        * ``Position_Right``: Position of the right circle.
    """

    def __init__(
        self, illusion_strength=0, difference=0, size_min=0.25, distance=1, distance_auto=False
    ):
        """
        Compute parameters for the Delboeuf Illusion.

        Parameters
        ----------
        illusion_strength : float
            The strength of the surrounding context, i.e. outer circles, in biasing perception of unequally sized inner circles. Defaults to 0.
            Specifically, the size of left outer circle relative to its inner circle (in percentage, e.g, if ``difference=1``,
            it means that the left outer circle will be 100% bigger, i.e., 2 times bigger than the left
            inner circle). A negative sign reflects the size difference of the right circles, i.e.,
            i.e., ``difference=-1`` means the right outer circle will be 100% bigger than the inner right circle.
        difference : float
            The objective size difference of the inner circles. Defaults to 0.
            Specifically, the size of left inner circle relative to the right inner circle (in percentage, e.g., if ``difference=1``,
            it means that the left circle will be 100% bigger, i.e., 2 times bigger than the right).
            A negative sign reflects the size difference of the right inner circle relative to the left,
            i.e., ``difference=-1`` means the right inner circle will be 100% bigger than the left inner circle.
        size_min : float
            Size of smaller inner circle. Defaults to 0.25.
        distance : float
            Distance between circles. Defaults to 1.
        distance_auto : bool
            If true, distance is between edges (fixed spacing), if false (default), between centers (fixed location).

        Returns
        -------
        dict
            Dictionary of parameters of the delboeuf illusion.

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> parameters = pyllusion.delboeuf_parameters()
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
        Returns a dictionary of parameters passed into the Delboeuf illusion.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, outline=10, background="white", **kwargs):
        """Create a PIL image of the Delboeuf illusion.
    
        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        outline : float
            The width of the outline of the circles in the illusion, passed into `image_circle()`.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `delboeuf_parameters()`.
    
        Returns
        -------
        Image
            Image of the Delboeuf illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).
    
        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> delboeuf = pyllusion.Delboeuf(illusion_strength=3)
        >>> delboeuf.to_image()
        """
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
        """Create a PsychoPy stimulus of the Delboeuf illusion.

        Parameters
        ----------
        window : object
            The window object initiated by `psychopy.visual.Window` in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `delboeuf_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).
    
        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event
    
        >>> # Create parameters
        >>> delboeuf = pyllusion.Delboeuf(difference=2, illusion_strength=3)
    
        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType='pygame', color='white')
    
        >>> # Display illusion
        >>> delboeuf.to_psychopy(window)
    
        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()

        """
        _delboeuf_psychopy(window, self.parameters, **kwargs)
