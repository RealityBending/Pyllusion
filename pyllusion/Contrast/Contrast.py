from .contrast_image import _contrast_image
from .contrast_parameters import _contrast_parameters
from .contrast_psychopy import _contrast_psychopy


class Contrast:
    """
    A class to generate the Simultaneous Contrast illusion.

    Simultaneous contrast, identified by Michel Eugène Chevreul, refers to the
    manner in which the colors of two different objects affect each other.
    Specifically, when comparing two targets with the same shade of grey, the one that is
    embedded against a darker background appears lighter than the other target embedded against a lighter background.

    Each instance of **Contrast** contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the background, i.e., contrasting colours, in biasing the perception of inner rectangles of different grey shades.
        Specifically, the difference in background colours, where large values create greater contrast in the two
        grey backgrounds.
        A positive sign means that the illusion will enhance the perception of the actual **difference** in brightness contrast
        of the two inner rectangles, whereas a negative sign reduces this perception.
    difference : float
        The objective difference of the grey shades of the two inner rectangles.
        Large positive signs reflect a darker lower rectangle relative to the upper rectangle, and negative signs reflect a darker upper
        rectangle relative to the lower rectangle.
    """

    def __init__(
        self, illusion_strength=0, difference=0
    ):
        """
        Compute parameters for the Simultaneous Contrast illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the background, i.e., contrasting colours, in biasing the perception of inner rectangles of different grey shades.
                Specifically, the difference in background colours, where large values create greater contrast in the two
                grey backgrounds.
                A positive sign means that the illusion will enhance the perception of the actual **difference** in brightness contrast
                of the two inner rectangles, whereas a negative sign reduces this perception.
            difference : float
                The objective difference of the grey shades of the two inner rectangles.
                Large positive signs reflect a darker lower rectangle relative to the upper rectangle, and negative signs reflect a darker upper
                rectangle relative to the lower rectangle.
        """
        self.parameters = _contrast_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the Simultaneous Contrast illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the Simultaneous Contrast illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of contrast_parameters().
            - **Illusion** : Name of the illusion, Contrast.
            - **Illusion_Strength** : The strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of contrast_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Rectangle_Top** : Luminance of the top inner rectangle.
            - **Rectangle_Bottom** : Luminance of the bottom inner rectangle.
            - **Background_Top** : Luminance of the top half of the background.
            - **Background_Bottom** : Luminance of the bottom half of the background.
            - **Rectangle_Top_RGB** : RGB value of the top inner rectangle.
            - **Rectangle_Bottom_RGB** : RGB value of the bottom inner rectangle.
            - **Background_Top_RGB** : RGB value of the top half of the background.
            - **Background_Bottom_RGB** : RGB value of the bottom half of the background.
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, **kwargs):
        """Create a PIL image of the Simultaneous Contrast illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        **kwargs
            Additional arguments passed into `contrast_parameters()`.

        Returns
        -------
        Image
            Image of the Simultaneous Contrast illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> contrast = pyllusion.Contrast(illusion_strength=-50, difference=0)
        >>> contrast.to_image()
        """

        img = _contrast_image(
            parameters=self.parameters,
            width=width,
            height=height,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the Simultaneous Contrast illusion.

        Parameters
        ----------
        window : object
            The window object in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `contrast_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> contrast = pyllusion.Contrast(difference=0, illusion_strength=-50)
        >>> parameters = contrast.get_parameters()

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType='pygame',
                                   color=parameters["Background_Top_RGB"],
                                   colorSpace='rgb255')

        >>> # Display illusion
        >>> contrast.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()

        """
        _contrast_psychopy(window, self.parameters, **kwargs)
