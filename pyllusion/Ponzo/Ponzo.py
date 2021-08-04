from .ponzo_image import _ponzo_image
from .ponzo_parameters import _ponzo_parameters
from .ponzo_psychopy import _ponzo_psychopy


class Ponzo:
    """
    A class to generate the Ponzo illusion.

    The Ponzo illusion is an optical illusion of relative size perception, where
    horizontal lines of identical size appear as different because of their surrounding context.
    Specifically, because we interpret the converging sides as mimicing railway tracks (i.e., upward-converging lines receding into the distance),
    the upper line appears longer than the shorter one.

    Each instance of `Ponzo` contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the tilting vertical lines in biasing the perception of horizontal lines of unequal lengths.
        Specifically, the angle of the vertical lines in degrees, i.e., `illusion_strength=20` represents
        a 20 degree tilt of the vertical lines.
        A negative sign means that the illusion will enhance the perception of the actual `difference`  in lengths
        whereas a positive sign reduces this perception.
    difference : float
        The objective length difference of the two horizontal lines.
        Specifically, the real difference of the upper horizontal line relative to the lower horizontal line. E.g.,
        if `difference=1` , the upper line will be 100% longer, i.e., 2 times longer than
        the lower line. A negative sign reflects the converse, where `difference=-1`
        will result in the lower line being 100% longer than the upper line.
        A negative sign would make the lower line longer than the upper line.
    size_min : float
        Length of shorter horizontal line. Defaults to 0.5.
    distance : float
        Distance between the upper and lower horizontal lines. Defaults to 1.
    """

    def __init__(
        self, illusion_strength=0, difference=0, size_min=0.5, distance=1
    ):
        """
        Compute parameters for the Ponzo illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the tilting vertical lines in biasing the perception of horizontal lines of unequal lengths.
                Specifically, the angle of the vertical lines in degrees, i.e., `illusion_strength=20` represents
                a 20 degree tilt of the vertical lines.
                A negative sign means that the illusion will enhance the perception of the actual `difference`  in lengths
                whereas a positive sign reduces this perception.
            difference : float
                The objective length difference of the two horizontal lines.
                Specifically, the real difference of the upper horizontal line relative to the lower horizontal line. E.g.,
                if `difference=1` , the upper line will be 100% longer, i.e., 2 times longer than
                the lower line. A negative sign reflects the converse, where `difference=-1`
                will result in the lower line being 100% longer than the upper line.
                A negative sign would make the lower line longer than the upper line.
            size_min : float
                Length of shorter horizontal line. Defaults to 0.5.
            distance : float
                Distance between the upper and lower horizontal lines. Defaults to 1.
        """
        self.parameters = _ponzo_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            size_min=size_min,
            distance=distance,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the Ponzo illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the Ponzo illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of ponzo_parameters()
            - **Illusion** : Name of the illusion, Ponzo.
            - **Illusion_Strength** : Strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of ponzo_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Distance** : Distance between the upper and lower horizontal lines, by modifying `distance` of ponzo_parameters().
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
            - **Size_Smaller** : Length of the shorter horizontal line, equates to `size_min` of ponzo_parameters().
            - **Side_Angle** : Angle of the converging vertical lines, equates to `illusion_strength` of ponzo_parameters().
            - **Side_Length** : Length of the converging vertical lines.
            - **Left_x1** : x-coordinate of the starting point (bottom) of the left converging line.
            - **Left_y1** : y-coordinate of the starting point (bottom) of the left converging line.
            - **Left_x2** : x-coordinate of the end point (top) of the left converging line.
            - **Left_y2** : y-coordinate of the end point (top) of the left converging line.
            - **Right_x1** : x-coordinate of the starting point (bottom) of the right converging line.
            - **Right_y1** : y-coordinate of the starting point (bottom) of the right converging line.
            - **Right_x2** : x-coordinate of the end point (top) of the right converging line.
            - **Right_y2** : y-coordinate of the end point (top) of the right converging line.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, outline=20, background="white", **kwargs):
        """Create a PIL image of the Ponzo illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        outline : float
            The width of the lines in the illusion, passed into `image_line()`.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `ponzo_parameters()`.

        Returns
        -------
        Image
            Image of the Ponzo illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> ponzo = pyllusion.Ponzo(illusion_strength=20)
        >>> ponzo.to_image()
        """
        img = _ponzo_image(
            parameters=self.parameters,
            width=width,
            height=height,
            outline=outline,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the Ponzo illusion.

        Parameters
        ----------
        window : object
            The window object in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `ponzo_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> ponzo = pyllusion.Ponzo(illusion_strength=20)

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pygame`, color="white")

        >>> # Display illusion
        >>> ponzo.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()

        """
        _ponzo_psychopy(window, self.parameters, **kwargs)
