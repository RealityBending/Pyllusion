from .poggendorff_image import _poggendorff_image
from .poggendorff_parameters import _poggendorff_parameters
from .poggendorff_psychopy import _poggendorff_psychopy


class Poggendorff:
    """
    A class to generate the Poggendorff illusion.

    The Poggendorff illusion is an optical illusion that involves the misperception
    of the position of one segment of a transverse line that has been interrupted
    by the contour of an intervening structure.

    Each instance of `Poggendorff` contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the line tilt in biasing the perception of an uncontinuous single line.
        Specifically, the orientation of the lines in degrees, 0 being vertical and
        larger values (in magnitude; no change with positive or negative sign) rotating clockwise.
        If `difference`  and `illusion_strength`  signs are opposite, it means that the illusion will enhance the perception of the actual `difference`  in line misalignement,
        whereas if the two parameters have the same signs, the illusion acts to reduce this perception.
    difference : float
        The objective magnitude of the lines discontinuity.
        Specifically, the amount of displacement of the right line relative to the left line. A positive sign
        represents the right line displaced higher up, and a negative sign represents it displaced lower down.
    """

    def __init__(
        self, illusion_strength=0, difference=0
    ):
        """
        Compute parameters for the Poggendorff illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the line tilt in biasing the perception of an uncontinuous single line.
                Specifically, the orientation of the lines in degrees, 0 being vertical and
                larger values (in magnitude; no change with positive or negative sign) rotating clockwise.
                If `difference`  and `illusion_strength`  signs are opposite, it means that the illusion will enhance the perception of the actual `difference`  in line misalignement,
                whereas if the two parameters have the same signs, the illusion acts to reduce this perception.
            difference : float
                The objective magnitude of the lines discontinuity.
                Specifically, the amount of displacement of the right line relative to the left line. A positive sign
                represents the right line displaced higher up, and a negative sign represents it displaced lower down.
        """
        self.parameters = _poggendorff_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the Poggendorff illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the Poggendorff illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of poggendorff_parameters()
            - **Illusion** : Name of the illusion, Poggendorff.
            - **Illusion_Strength** : Strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of poggendorff_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Left_x1** : x-coordinate of the starting point (from centre) of the left line segment.
            - **Left_y1** : y-coordinate of the starting point (from centre) of the left line segment.
            - **Left_x2** : x-coordinate of the end point (leftwards) of the left line segment.
            - **Left_y2** : y-coordinate of the end point (leftwards) of the left line segment.
            - **Right_x1** : x-coordinate of the starting point (from centre) of the right line segment.
            - **Right_y1** : y-coordinate of the starting point (from centre) of the right line segment.
            - **Right_x2** : x-coordinate of the end point (rightwards) of the right line segment.
            - **Right_y2** : y-coordinate of the end point (rightwards) of the right line segment.
            - **Angle** : Angle displacement of the transverse line from horizontal.
            - **Rectangle_Height** : Height of rectangle.
            - **Rectangle_Width** : Width of rectangle.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, background="white", **kwargs):
        """Create a PIL image of the Poggendorff illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `poggendorff_parameters()`.

        Returns
        -------
        Image
            Image of the Poggendorff illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> poggendorff = pyllusion.Poggendorff(illusion_strength=-55)
        >>> poggendorff.to_image()

        """
        img = _poggendorff_image(
            parameters=self.parameters,
            width=width,
            height=height,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the Poggendorff illusion.

        Parameters
        ----------
        window : object
            The window object in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `poggendorff_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> poggendorff = pyllusion.Poggendorff(illusion_strength=-50)

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pygame`, color="white")

        >>> # Display illusion
        >>> poggendorff.to_psychopy(window=window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()
        """
        _poggendorff_psychopy(window, self.parameters, **kwargs)
