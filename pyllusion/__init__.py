"""
The Pyllusion module.
"""
__version__ = "0.0.12"

# Import Illusions
from .Contrast import *
from .Delboeuf import *
from .Ebbinghaus import *
from .Autostereogram import *
from .Pareidolia import *
from .RodFrame import *
from .VerticalHorizontal import *
from .White import *
from .Zollner import *
from .MullerLyer import *
from .Poggendorff import *
from .Ponzo import *

# Import submodules
from .image import *
from .movement import *
from .psychopy import *

# Maintainer info
__author__ = "The Reality Bending League"
__email__ = "dom.makowski@gmail.com"

# Get path of stimuli images
# import inspect
# pyllusion_path = inspect.getfile(autostereogram)  # Get path of a random function
# pyllusion_path = pyllusion_path.split("autostereogram.py")[0]
# pyllusion_path = pyllusion_path + "stimuli\\"
