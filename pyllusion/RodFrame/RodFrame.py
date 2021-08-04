from .rodframe_image import _rodframe_image
from .rodframe_parameters import _rodframe_parameters
from .rodframe_psychopy import _rodframe_psychopy


class RodFrame:
    """
    A class to generate the vertical-horizontal illusion.

    The Rod and frame illusion is an optical illusion causing the participant to
    perceive the rod to be oriented congruent with the orientation of the frame.

    Each instance of `RodFrame`  contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the frame tilt in biasing the perception of a congruently tilted rod.
        A negative sign means that the illusion will enhance the perception of the actual `difference`  in angle alignment
        whereas a positive sign reduces this perception.
    difference : float
        The objective tilt of the rod.
        Specifically, the orientation of the rod in degrees, 0 being vertical and positive values rotating clockwise, and
        negative values rotating anticlockwise.
    """

    def __init__(
        self, illusion_strength=0, difference=0, size_min=0.5
    ):
        """
        Compute Parameters for the Rod and Frame Illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the frame tilt in biasing the perception of a congruently tilted rod.
                A negative sign means that the illusion will enhance the perception of the actual `difference` in angle alignment
                whereas a positive sign reduces this perception.
            difference : float
                The objective tilt of the rod.
                Specifically, the orientation of the rod in degrees, 0 being vertical and positive values rotating clockwise, and
                negative values rotating anticlockwise.
        """
        self.parameters = _rodframe_parameters(
            illusion_strength=illusion_strength,
            difference=difference
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the Rod and Frame illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the Rod and Frame illusion. including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of rodframe_parameters()
            - **Illusion** : Name of the illusion, RodFrame.
            - **Illusion_Strength** : Strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of rodframe_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Rod_Angle** : Angle of the rod, equates to `difference` passed into rodframe_parameters().
            - **Frame_Angle** : Angle of the frame.
            - **Angle_Difference** : the angle difference between the rod and the frame.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, outline=20, background="white", **kwargs):
        """Create a PIL image of the Rod and frame illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        outline : float
            The width of the rod in the illusion, passed into `image_line()`, and the width of the
            rectangle border, passed into `image_rectangle()`.
        background : str
            Color of the background.
        **kwargs
            Additional arguments passed into `rodframe_parameters()`.

        Returns
        -------
        Image
            Image of the Rod and frame illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> rodframe = pyllusion.RodFrame(illusion_strength=65, difference=0)
        >>> rodframe.to_image()
        """
        img = _rodframe_image(
            parameters=self.parameters,
            width=width,
            height=height,
            outline=outline,
            background=background,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the Rod and Frame illusion.

        Parameters
        ----------
        window : object
            The window object in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `rodframe_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> rodframe = pyllusion.RodFrame(illusion_strength=65, difference=0)

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pygame`, color=`white`)

        >>> # Display illusion
        >>> rodframe.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()
        """
        _rodframe_psychopy(window, self.parameters, **kwargs)
