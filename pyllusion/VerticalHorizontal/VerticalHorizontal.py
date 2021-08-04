from .verticalhorizontal_image import _verticalhorizontal_image
from .verticalhorizontal_parameters import _verticalhorizontal_parameters
from .verticalhorizontal_psychopy import _verticalhorizontal_psychopy


class VerticalHorizontal:
    """
    A class to generate the vertical-horizontal illusion.

    The vertical–horizontal illusion illustrates the tendency for observers to overestimate
    the length of a vertical line relative to a horizontal line of the same length.

    Each instance of `MullerLyer` contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the tilted vertical line in biasing the overestimation of its length relative to the horizontal line.
        Specifically, the orientation of the line in degrees, 0 being vertical and
        values rotating anticlockwise if the left line is rotated and clockwise if the right line is rotated.
        A negative sign means that the illusion will enhance the perception of the actual `difference` in lengths
        whereas a positive sign reduces this perception.
    difference : float
        The objective length difference of the vertical and horizontal lines.
        Specifically, the real difference of left line relative to the right line. E.g.,
        if `difference=1`, the left line will be 100% longer, i.e., 2 times longer than
        the right line. A negative sign would make the right line longer than the left line.
    size_min : float
        Length of the shorter line. Defaults to 0.5.
    """

    def __init__(
        self, illusion_strength=0, difference=0, size_min=0.5
    ):
        """Compute Parameters for vertical-horizontal illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the tilted vertical line in biasing the overestimation of its length relative to the horizontal line.
                Specifically, the orientation of the line in degrees, 0 being vertical and
                values rotating anticlockwise if the left line is rotated and clockwise if the right line is rotated.
                A negative sign means that the illusion will enhance the perception of the actual `difference` in lengths
                whereas a positive sign reduces this perception.
            difference : float
                The objective length difference of the vertical and horizontal lines.
                Specifically, the real difference of left line relative to the right line. E.g.,
                if `difference=1`, the left line will be 100% longer, i.e., 2 times longer than
                the right line. A negative sign would make the right line longer than the left line.
            size_min : float
                Length of the shorter line. Defaults to 0.5.
        """
        self.parameters = _verticalhorizontal_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            size_min=size_min,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the vertical-horizontal illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the vertical-horizontal illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of verticalhorizontal_parameters()
            - **Illusion** : Name of the illusion, VerticalHorizontal.
            - **Illusion_Strength** : Strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of verticalhorizontal_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Left_x1** : x-coordinate of the starting point of the left line.
            - **Left_y1** : y-coordinate of the starting point of the left line.
            - **Left_x2** : x-coordinate of the end point of the left line.
            - **Left_y2** : y-coordinate of the end point of the left line.
            - **Left_Angle** : The angle in which the left line is rotated.
            - **Right_x1** : x-coordinate of the starting point of the right line.
            - **Right_y1** : y-coordinate of the starting point of the right line.
            - **Right_x2** : x-coordinate of the end point of the right line.
            - **Right_y2** : y-coordinate of the end point of the right line.
            - **Right_Angle** : The angle in which the right line is rotated.
            - **Size_Left** : Length of the left line.
            - **Size_Right** : Length of the right line.
            - **Size_Larger** : Length of the longer line.
            - **Size_Smaller** : Length of the shorter line, equates to `size_min` of verticalhorizontal_parameters().
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, background="white", **kwargs):
        """Create a PIL image of the vertical-horizontal illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `verticalhorizontal_parameters()`.

        Returns
        -------
        Image
            Image of the vertical-horizontal illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> verticalhorizontal = pyllusion.VerticalHorizontal(illusion_strength=20)
        >>> verticalhorizontal.to_image()
        """
        img = _verticalhorizontal_image(
            parameters=self.parameters,
            width=width,
            height=height,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the vertical-horizontal illusion.

        Parameters
        ----------
        window : object
            The window object in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `verticalhorizontal_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> verticalhorizontal = pyllusion.VerticalHorizontal(illusion_strength=90)

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pygame`, color=`white`)

        >>> # Display illusion
        >>> verticalhorizontal.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()
        """
        _verticalhorizontal_psychopy(window, self.parameters, **kwargs)
