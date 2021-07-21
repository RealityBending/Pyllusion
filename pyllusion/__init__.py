"""
The Pyllusion module.
"""
__version__ = "0.0.11"

# Import Illusions
from .Delboeuf import *
from .Ebbinghaus import *
from .MullerLyer import *
from .Ponzo import *
from .VerticalHorizontal import *
from .RodFrame import *
from .Poggendorff import *
from .Zollner import *
from .Contrast import *
from .White import *

# Import submodules
from .illusion import *
from .image import *
from .movement import *
from .MullerLyer import *
from .Poggendorff import *
from .Ponzo import *
from .psychopy import *
from .RodFrame import *
from .VerticalHorizontal import *


# Maintainer info
__author__ = "The Reality Bending League"
__email__ = "dom.makowski@gmail.com"

# Get path of stimuli images
# import inspect
# pyllusion_path = inspect.getfile(autostereogram)  # Get path of a random function
# pyllusion_path = pyllusion_path.split("autostereogram.py")[0]
# pyllusion_path = pyllusion_path + "stimuli\\"
