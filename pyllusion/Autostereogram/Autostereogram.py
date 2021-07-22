import numpy as np
import PIL.Image, PIL.ImageDraw, PIL.ImageFilter, PIL.ImageFont, PIL.ImageOps

from ..image import image_noise, image_text


class Autostereogram:
    """
    A class to generate Autostereograms based on a given depth map.

    Autostereograms are images made of a pattern that is horizontally repeated (with slight variations)
    which, when watched with the appropriate focus, will generate an illusion of depth.
    """
    def __init__(
        self, stimulus="Hello", pattern=None, n_repetitions=14, depth=1, invert=False, **kwargs
    ):

        self.stimulus = stimulus
        self.pattern = pattern
        self.n_repetitions = n_repetitions
        self.depth = depth
        self.invert = invert

        # If '/' and '.' in string, we assume it's a path
        if "/" in self.stimulus and "." in self.stimulus:
            depth_map = PIL.Image.open(self.stimulus)
        else:  # Else a text
            depth_map = image_text(text=self.stimulus, **kwargs)

        # Convert to black and white
        depth_map = depth_map.convert('L')
        depth_map = PIL.ImageOps.autocontrast(depth_map)
    
        if invert is False:
            self.depth_map = PIL.ImageOps.invert(depth_map)

        # Get size of depth map
        self.width, self.height = self.depth_map.size
    
        # We want the strip width to be a multiple of the tile
        # width so it repeats cleanly.
        self.strip_width = int(self.width / self.n_repetitions)
    
        # Fix conflicting arguments
        conflicting_args = ["width", "height", "font"]
        kwargs = {key: kwargs[key] for key in kwargs if key not in conflicting_args}
    
        # Create strip of pattern
        if pattern is None:
            strip = image_noise(width=self.strip_width, height=self.height, **kwargs)
        else:
            strip = self.pattern(width=self.strip_width, height=self.height, **kwargs)
        self.strip_pixels = strip.load()
    

    def draw(self, guide=True):
        """Create a PIL image of Autostereograms.
    
        Parameters
        ----------
        guide : bool
            Defaults to 'True' to activate two red dots as guidance, and 'False' to disable the guide.
    
        Returns
        -------
        Image
            Image of the Autostereograms illusion, defaults to 800 x 600 pixels.
            Can be resized
            (`resize()`, See https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.resize)
            and saved in different file formats
            (`save()` See https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).
    
        Examples
        ---------
        >>> import pyllusion
        >>>
        >>> autostereograms = pyllusion.Autostereogram(stimulus="3D", width=1000, height=500, font="arialbd.ttf")
        >>> autostereograms.draw(guide=True)
        """

        image = PIL.Image.new("RGB", (self.width, self.height))

        # Load pixels for easy replacement
        depth_pixels = self.depth_map.load()
        image_pixels = image.load()
    
        for x in range(self.width):
            for y in range(self.height):
                # Need one full strip's worth to borrow from.
                if x < self.strip_width:
                    image_pixels[x, y] = self.strip_pixels[x, y]
                else:
                    shift_amplitude = self.depth * (depth_pixels[x, y] / self.n_repetitions)
                    image_pixels[x, y] = image_pixels[x - self.strip_width + shift_amplitude, y]
    
        # Add guide
        if guide is True:
            draw = PIL.ImageDraw.Draw(image)
            for i in [-2, 0]:
                diameter = 0.005 * self.width
                center_x = (self.width / 2) + (i * self.strip_width / 2)
                center_y = 0.5 * self.height
                draw.ellipse([center_x-diameter, center_y-diameter, center_x+diameter, center_y+diameter], fill=(255, 0, 0))
        return image
