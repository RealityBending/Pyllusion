"""
The Pyllusion module.
"""
__version__ = "1.2"

from .Autostereogram import *

# Import Illusions
from .Contrast import *
from .Delboeuf import *
from .Ebbinghaus import *

# Import submodules
from .image import *
from .movement import *
from .MullerLyer import *
from .Pareidolia import *
from .Poggendorff import *
from .Ponzo import *
from .psychopy import *
from .RodFrame import *
from .utilities import *
from .VerticalHorizontal import *
from .White import *
from .Zollner import *

# Maintainer info
__author__ = "The Reality Bending League"
__email__ = "dom.makowski@gmail.com"

# Get path of stimuli images
# import inspect
# pyllusion_path = inspect.getfile(autostereogram)  # Get path of a random function
# pyllusion_path = pyllusion_path.split("autostereogram.py")[0]
# pyllusion_path = pyllusion_path + "stimuli\\"
