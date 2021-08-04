from .white_image import _white_image
from .white_parameters import _white_parameters
from .white_psychopy import _white_psychopy


class White:
    """
    A class to generate the White's illusion.

    White’s illusion is a brightness illusion in which rectangles of the same grey
    color are perceived of different luminance depending on their background.
    Specifically, rectangles embedded against a darker background appears lighter
    than the rectangles embedded against a lighter background.

    Each instance of `White` contains attributes corresponding to the parameters of the illusion.

    Parameters
    ----------
    illusion_strength : float
        The strength of the background, i.e., contrasting colours, in biasing the perception of inner rectangles of different grey shades.
        Specifically, the difference in background colours, where large values create greater contrast in the two
        grey backgrounds.
        A positive sign means that the illusion will enhance the perception of the actual `difference` in brightness contrast
        of the two inner rectangles, whereas a negative sign reduces this perception.
    difference : float
        The objective difference of the grey shades of the two inner rectangles.
        Specifically, the brightness of the left grey rectangles relative to the right grey rectangles.
        Large positive signs correspond to brighter left rectangles and negative signs correspond to brighter right rectangles.
    strips_n : int
        Number of rows of contrasting segments. Defaults to 9.
    """

    def __init__(
        self, illusion_strength=0, difference=0, strips_n=9
    ):
        """
        Compute parameters for the White`s illusion.

        Parameters
        ----------
            illusion_strength : float
                The strength of the background, i.e., contrasting colours, in biasing the perception of inner rectangles of different grey shades.
                Specifically, the difference in background colours, where large values create greater contrast in the two
                grey backgrounds.
                A positive sign means that the illusion will enhance the perception of the actual `difference` in brightness contrast
                of the two inner rectangles, whereas a negative sign reduces this perception.
            difference : float
                The objective difference of the grey shades of the two inner rectangles.
                Specifically, the brightness of the left grey rectangles relative to the right grey rectangles.
                Large positive signs correspond to brighter left rectangles and negative signs correspond to brighter right rectangles.
            strips_n : int
                Number of rows of contrasting segments. Defaults to 9.
        """
        self.parameters = _white_parameters(
            illusion_strength=illusion_strength,
            difference=difference,
            strips_n=strips_n,
        )

    def get_parameters(self):
        """
        Returns a dictionary of parameters passed into the White`s illusion.

        Returns
        -------
        dict
            Dictionary of parameters of the White`s illusion, including:

            - **Difference** : Objective difference in the target features, by modifying `difference` of white_parameters()
            - **Illusion** : Name of the illusion, White's.
            - **Illusion_Strength** : Strength of the surrounding context in biasing illusion, by modifying `illusion_strength` of white_parameters().
            - **Illusion_Type** : `Congruent` if the illusion enhances the perception of the objective difference in the illusion, and `Incongruent` if it reduces the perceived difference.
            - **Target1** : Luminance of the left grey rectangles.
            - **Target2** : Luminance of the right grey rectangle.
            - **Background1** : Luminance of the background that `Target1` is embedded in.
            - **Background2** : Luminance of the background that `Target2` is embedded in.
            - **Target1_RGB** : RGB value of the left grey rectangles.
            - **Target2_RGB** : RGB value of the right grey rectangle.
            - **Background1_RGB** : RGB value of the background that `Target1` is embedded in.
            - **Background2_RGB** : RGB value of the background that `Target2` is embedded in.
            - **Target1_y** : y-coordinates of the left grey rectangles.
            - **Target2_y** : y-coordinates of the right grey rectangles.
            - **Target_Height** : Height of each strip of rectangular segment.
            - **Target_n** : Number of horizontal rectangular segments, equates to `strips_n` in white_parameters().
        """
        return self.parameters

    def to_dict(self):
        """
        Alias for `get_parameters()`.
        """
        return self.get_parameters()

    def to_image(self, width=800, height=600, **kwargs):
        """Create a PIL image of the White`s illusion.

        Parameters
        ----------
        width : int
            Width of the returned image.
        height : int
            Height of the returned image.
        **kwargs
            Additional arguments passed into `white_parameters()`.

        Returns
        -------
        Image
            Image of the white illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> white = pyllusion.White(difference=0, illusion_strength=100)
        >>> white.to_image()
        """
        img = _white_image(
            parameters=self.parameters,
            width=width,
            height=height,
            **kwargs
        )
        return img

    def to_psychopy(self, window, **kwargs):
        """Create a PsychoPy stimulus of the White`s illusion.

        Parameters
        ----------
        window : object
            The window object initiated by `psychopy.visual.Window` in which the stimulus will be rendered.
        **kwargs
            Additional arguments passed into `white_parameters()`.

        Returns
        -------
        In-place modification of the PsychoPy window (No explicit return).

        Examples
        ---------
        >>> import pyllusion
        >>> from psychopy import visual, event

        >>> # Create parameters
        >>> white = pyllusion.White(difference=0, illusion_strength=100)
        >>> parameters = white.get_parameters()

        >>> # Initiate Window
        >>> window = visual.Window(size=[800, 600], winType=`pygame`,
                                   color=parameters["Background1_RGB"], colorSpace=`rgb255`)

        >>> # Display illusion
        >>> white.to_psychopy(window)

        >>> # Refresh and close window
        >>> window.flip()
        >>> event.waitKeys()  # Press any key to close
        >>> window.close()

        """
        _white_psychopy(window, self.parameters, **kwargs)
