import numpy as np
import PIL.Image

from ..image.image_blob import image_blobs


class Pareidolia:
    """
    A class to create (pseudo)noise images.

    Pareidolia is the tendency to incorrectly perceive of a stimulus as an object
    pattern or meaning known to the observer. To create stimuli for the observation
    of such phenomenon, this function creates pure-noise images using bivariate
    Gaussian blobs with different standard deviations (SD).

    """
    def __init__(
        self, pattern=None, n=[10, 1000], sd=[20, 2], weight=[2, 1], alpha=80, blur=30,
    ):

        self.pattern = pattern
        self.n = n
        self.sd = sd
        self.weight = weight
        self.alpha = alpha
        self.blur = blur

        # Load pattern
        if self.pattern is None:
            self.image = PIL.Image.new("RGBA", (500, 500), "WHITE")
        elif isinstance(self.pattern, tuple):
            self.image = PIL.Image.new("RGBA", self.pattern, "WHITE")
        elif isinstance(self.pattern, PIL.Image.Image) is False:
            self.image = PIL.Image.open(self.pattern)
        self.width, self.height = self.image.size
    
    def draw(self, negative=False):
        """Create a PIL image of a Pareidolia image.
    
        Parameters
        ----------
        negative : bool
            Activate 'True' to invert pixel values (negative-positive inverting) of an image. Defaults to 'False'.
            Passed to ``PIL.ImageOps.invert``.
    
        Returns
        -------
        Image
            Image of the Pareidolia image, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).
    
        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> pareidolia = pyllusion.Pareidolia((480, 480), n=[20, 300, 4000], sd=[4, 2, 1], weight=[3, 2, 1], alpha=80, blur=0.5)
        >>> pareidolia.draw()  #doctest: +ELLIPSIS
        <PIL.Image.Image ...>
        """

        # Convert to black and white RGB (with white background)
        img = PIL.Image.new("RGBA", self.image.size, "WHITE")
        img.paste(self.image, (0, 0), self.image)
        img = img.convert('RGB')
    
        # Make it negative if need be
        if negative is True:
            img = PIL.ImageOps.invert(img)
    
        # Blur the image
        img = img.filter(PIL.ImageFilter.GaussianBlur(self.blur / 100 * self.width))
    
        # Generate noise
        self.sd = np.array(self.sd) / 100 * self.width
        noise = image_blobs(img.size, n=self.n, sd=self.sd, weight=self.weight).convert("RGB")

        # Blend with noise
        stim = PIL.Image.blend(img, noise, alpha=self.alpha / 100)

        # Normalize
        stim = PIL.ImageOps.autocontrast(stim)
    
        return stim
