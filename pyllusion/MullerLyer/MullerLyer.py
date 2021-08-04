from .mullerlyer_image import _mullerlyer_image
from .mullerlyer_parameters import _mullerlyer_parameters
from .mullerlyer_psychopy import _mullerlyer_psychopy


class MullerLyer:
    """
    A class to generate the Müller-Lyer illusion.

    The Müller-Lyer illusion is an optical illusion causing the participant to
    perceive two segments as being of different length depending on the shape of
    the arrows. Specifically, the line with outward-protruding fins appears longer than
    the line with inward-protruding fins.

    Each instance of `MullerLyer`  contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the arrow shapes (or fins) in biasing the perception of lines of unequal lengths.
        Specifically, the angle of the fins in degrees, i.e., `illusion_strength=20`  represents
        a 20 degree tilt (away from vertical) of the fins.
        A negative sign means that the illusion will enhance the perception of the actual `difference`  in lengths
        whereas a positive sign reduces this perception.
    difference : float
        The objective length difference of the horizontal lines.
        Specifically, the real difference of upper horizontal line relative to the lower horizontal line. E.g.,
        if `difference=1`, the upper line will be 100% longer, i.e., 2 times longer than the lower line.
        A negative sign would make the lower line longer than the upper line.
    size_min : float
        Length of lower horizontal line.
    distance : float
        Distance between the upper and lower horizontal lines.
    """

    def __init__(
        self, illusion_strength=0, difference=0, size_min=0.5, distance=1
    ):
        """
        Compute parameters for the Müller-Lyer illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the arrow shapes (or fins) in biasing the perception of lines of unequal lengths.
                Specifically, the angle of the fins in degrees, i.e., `illusion_strength=20`  represents
                a 20 degree tilt (away from vertical) of the fins.
                A negative sign means that the illusion will enhance the perception of the actual `difference`  in lengths
                whereas a positive sign reduces this perception.
            difference : float
                The objective length difference of the horizontal lines.
                Specifically, the real difference of upper horizontal line relative to the lower horizontal line. E.g.,
                if `difference=1`, the upper line will be 100% longer, i.e., 2 times longer than the lower line.
                A negative sign would make the lower line longer than the upper line.
            size_min : float
                Length of lower horizontal line.
            distance : float
                Distance between the upper and lower horizontal lines.
        """
        self.parameters = _mullerlyer_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            size_min=size_min,
            distance=distance,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the Müller-Lyer illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the Müller-Lyer illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of mullerlyer_parameters()
            - **Illusion** : Name of the illusion, MullerLyer.
            - **Illusion_Strength** : The strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of mullerlyer_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference
            - **Distance** : Distance between the upper and lower horizontal lines, by modifying `distance` of mullerlyer_parameters()`.
            - **Bottom_x1** : x-coordinate of the starting point (left) of the lower horizontal line.
            - **Bottom_y1** : y-coordinate of the starting point (left) of the lower horizontal line.
            - **Bottom_x2** : x-coordinate of the end point (right) of the lower horizontal line.
            - **Bottom_y2** : y-coordinate of the end point (right) of the lower horizontal line.
            - **Top_x1** : x-coordinate of the starting point (left) of the upper horizontal line.
            - **Top_y1** : y-coordinate of the starting point (left) of the upper horizontal line.
            - **Top_x2** : x-coordinate of the end point (right) of the upper horizontal line.
            - **Top_y2** : y-coordinate of the end point (right) of the upper horizontal line.
            - **Size_Bottom** : Length of the lower horizontal line.
            - **Size_Top** : Length of the upper horizontal line.
            - **Size_Larger** : Length of the longer horizontal line.
            - **Size_Smaller** : Length of the shorter horizontal line, equates to `size_min` of mullerlyer_parameters().
            - **Distractor_Length** : Length of the distractor fins. Equivalent to half the length of `size_min` passed into mullerlyer_parameters().
            - **Distractor_TopLeft_*** : x- and y- coordinates of the top left fins.
            - **Distractor_TopRight_*** : x- and y- coordinates of the top right fins.
            - **Distractor_BottomLeft_*** : x- and y- coordinates of the bottom left fins.
            - **Distractor_BottomRight_*** : x- and y- coordinates of the bottom right fins.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, outline=20, background="white", **kwargs):
        """
        Create a PIL image of the Müller-Lyer illusion.

        Parameters
        ----------
        parameters : dict
            Parameters of the Müller-Lyer illusion generated by `mullerlyer_parameters()`.
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        outline : float
            The width of the lines in the illusion, passed into `image_line()`.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `mullerlyer_parameters()`.

        Returns
        -------
        Image
            Image of the Müller-Lyer illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> mullerlyer = pyllusion.MullerLyer(difference=0.5, illusion_strength=20)
        >>> mullerlyer.to_image()
        """
        img = _mullerlyer_image(
            parameters=self.parameters,
            width=width,
            height=height,
            outline=outline,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the Müller-Lyer illusion.

        Parameters
        ----------
        window : object
            The window object initiated by `psychopy.visual.Window` in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `mullerlyer_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> mullerlyer = pyllusion.MullerLyer(difference=0.5, illusion_strength=20)

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pygame`, color=`white`)

        >>> # Display illusion
        >>> mullerlyer.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()

        """
        _mullerlyer_psychopy(window, self.parameters, **kwargs)
