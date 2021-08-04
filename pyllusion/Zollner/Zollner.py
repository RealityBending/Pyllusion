from .zollner_image import _zollner_image
from .zollner_parameters import _zollner_parameters
from .zollner_psychopy import _zollner_psychopy


class Zollner:
    """
    A class to generate the Zöllner illusion.

    The Zöllner illusion is an optical illusion, where horizontal lines are perceived
    as not parallel because of their background (i.e., the slanting of the intersecting lines).

    Each instance of `Zollner` contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the background, i.e., tilted distractor lines, in biasing the perception of unparallel horizontal lines.
        Specifically, the angle of the distractor lines in degrees (relative to vertical), where larger values
        increase susceptibility to the illusion.
        A positive sign means that the illusion will enhance the perception of the actual `difference` in slantness of the horizontal lines
        whereas a negative sign reduces this perception.
    difference : float
        The objective parallel alignment of the two horizontal lines.
        Specifically, the angle of the two horizontal target lines in degrees, where `difference=10` represents
        a 10 degree tilt of the lines towards each other (converging towards the right side of the pane). A negative sign
        flips the direction of the convergence (converging towards the left side of the pane).
    distractors_n : int
        Number of distractor lines in the background. Defaults to 8.
    distractors_length : float
        Length of distractor lines in the background. Defaults to 0.66.
    """

    def __init__(
        self, illusion_strength=0, difference=0, distractors_n=8, distractors_length=0.66
    ):
        """
        Compute parameters for the Zöllner illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the background, i.e., tilted distractor lines, in biasing the perception of unparallel horizontal lines.
                Specifically, the angle of the distractor lines in degrees (relative to vertical), where larger values
                increase susceptibility to the illusion.
                A positive sign means that the illusion will enhance the perception of the actual `difference` in slantness of the horizontal lines
                whereas a negative sign reduces this perception.
            difference : float
                The objective parallel alignment of the two horizontal lines.
                Specifically, the angle of the two horizontal target lines in degrees, where `difference=10` represents
                a 10 degree tilt of the lines towards each other (converging towards the right side of the pane). A negative sign
                flips the direction of the convergence (converging towards the left side of the pane).
            distractors_n : int
                Number of distractor lines in the background. Defaults to 8.
            distractors_length : float
                Length of distractor lines in the background. Defaults to 0.66.
        """
        self.parameters = _zollner_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            distractors_n=distractors_n,
            distractors_length=distractors_length,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the Zollner illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the Zöllner illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of zollner_parameters()
            - **Illusion** : Name of the illusion, Zollner.
            - **Illusion_Strength** : Strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of zollner_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Top_x1** : x-coordinate of the starting point (left) of the upper horizontal line.
            - **Top_y1** : y-coordinate of the starting point (left) of the upper horizontal line.
            - **Top_x2** : x-coordinate of the end point (right) of the upper horizontal line.
            - **Top_y2** : y-coordinate of the end point (right) of the upper horizontal line.
            - **Bottom_x1** : x-coordinate of the starting point (left) of the lower horizontal line.
            - **Bottom_y1** : y-coordinate of the starting point (left) of the lower horizontal line.
            - **Bottom_x2** : x-coordinate of the end point (right) of the lower horizontal line.
            - **Bottom_y2** : y-coordinate of the end point (right) of the lower horizontal line.
            - **Distractors_n** : Number of intersecting distractor lines, equates to `distractors_n` of zollner_parameters().
            - **Distractors_Size** : Length of intersecting distractor lines, equates to `distractors_length` of zollner_parameters().
            - **Distractors_Angle** : Angle of the intersecting distractor lines (relative to vertical).
            - **Distractors_Top_*** : x- and y- coordinates of the starting points and end points of the top distractor lines.
            - **Distractors_Bottom_*** : x- and y- coordinates of the starting points and end points of the bottom distractor lines.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, background="white", **kwargs):
        """Create a PIL image of the Zöllner illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `zollner_parameters()`.

        Returns
        -------
        Image
            Image of the Zöllner illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> zollner = pyllusion.Zollner(illusion_strength=75)
        >>> zollner.to_image()
        """
        img = _zollner_image(
            parameters=self.parameters,
            width=width,
            height=height,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the Zöllner illusion.

        Parameters
        ----------
        window : object
            The window object in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `zollner_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> zollner = pyllusion.Zollner(illusion_strength=75)

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pyglet`, color=`white`)

        >>> # Display illusion
        >>> zollner.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()

        """
        _zollner_psychopy(window, self.parameters, **kwargs)
